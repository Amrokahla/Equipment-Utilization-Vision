from __future__ import annotations

import base64
import logging
import signal
import time
from datetime import datetime, timezone

import cv2

from .adapters.video_reader import VideoReader
from .config import Settings
from .producer import FrameProducer

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = 100


class IngestionService:
    """Reads a video source, encodes frames, and publishes to Kafka."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._source_id = settings.source_id or self._derive_source_id(
            settings.video_source_path
        )
        self._reader = VideoReader(settings.video_source_path)
        self._producer = FrameProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            topic=settings.kafka_raw_frames_topic,
        )
        self._running = False
        self._counters = {
            "frames_read": 0,
            "frames_published": 0,
            "frames_skipped": 0,
            "encode_errors": 0,
        }

    @staticmethod
    def _derive_source_id(path: str) -> str:
        from pathlib import Path
        return Path(path).stem

    # ------------------------------------------------------------------

    def run(self) -> None:
        self._running = True
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        logger.info("Starting ingestion (source_id=%s)", self._source_id)
        self._reader.open()

        try:
            for frame_number, frame_bgr in self._reader.read():
                if not self._running:
                    logger.info("Stopped by signal")
                    break

                self._counters["frames_read"] += 1

                if frame_number % self._settings.frame_stride != 0:
                    self._counters["frames_skipped"] += 1
                    continue

                encoded = self._encode(frame_number, frame_bgr)
                if encoded is None:
                    continue

                message = {
                    "source_id": self._source_id,
                    "frame_number": frame_number,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "width": self._reader.width,
                    "height": self._reader.height,
                    "fps": self._reader.fps,
                    "encoding": "jpeg_base64",
                    "frame_data": encoded,
                }

                self._producer.produce(message)
                self._counters["frames_published"] += 1

                if self._counters["frames_published"] % HEARTBEAT_INTERVAL == 0:
                    self._log_heartbeat()

                if self._settings.ingest_loop_sleep_ms > 0:
                    time.sleep(self._settings.ingest_loop_sleep_ms / 1000.0)
        finally:
            self._shutdown()

    # ------------------------------------------------------------------

    def _encode(self, frame_number: int, frame_bgr) -> str | None:  # noqa: ANN001
        try:
            ok, buf = cv2.imencode(
                ".jpg",
                frame_bgr,
                [cv2.IMWRITE_JPEG_QUALITY, self._settings.jpeg_quality],
            )
            if not ok:
                self._counters["encode_errors"] += 1
                logger.warning("imencode returned False at frame %d", frame_number)
                return None
            return base64.b64encode(buf.tobytes()).decode("ascii")
        except Exception:
            self._counters["encode_errors"] += 1
            logger.exception("Encode error at frame %d", frame_number)
            return None

    def _log_heartbeat(self) -> None:
        c = self._counters
        logger.info(
            "Heartbeat: source=%s published=%d read=%d skipped=%d errors=%d "
            "delivered=%d failed=%d",
            self._source_id,
            c["frames_published"],
            c["frames_read"],
            c["frames_skipped"],
            c["encode_errors"],
            self._producer.delivered_count,
            self._producer.failed_count,
        )

    def _shutdown(self) -> None:
        logger.info("Shutting down ingestion service…")
        self._reader.close()
        self._producer.flush()
        c = self._counters
        logger.info(
            "Final: read=%d published=%d skipped=%d encode_errors=%d "
            "delivered=%d failed=%d",
            c["frames_read"],
            c["frames_published"],
            c["frames_skipped"],
            c["encode_errors"],
            self._producer.delivered_count,
            self._producer.failed_count,
        )

    def _handle_signal(self, signum: int, _frame) -> None:  # noqa: ANN001
        logger.info("Received signal %d — stopping", signum)
        self._running = False
