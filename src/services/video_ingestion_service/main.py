from __future__ import annotations

import logging
import sys

from .config import settings
from .service import IngestionService

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("ingestion")


def main() -> None:
    logger.info("Video Ingestion Service starting")
    logger.info("  source : %s", settings.video_source_path)
    logger.info("  topic  : %s", settings.kafka_raw_frames_topic)
    logger.info("  stride : %d", settings.frame_stride)
    logger.info("  quality: %d", settings.jpeg_quality)

    try:
        svc = IngestionService(settings)
        svc.run()
    except FileNotFoundError:
        logger.error(
            "Video file not found: %s — mount it via the data/ volume",
            settings.video_source_path,
        )
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)

    logger.info("Video Ingestion Service finished")


if __name__ == "__main__":
    main()
