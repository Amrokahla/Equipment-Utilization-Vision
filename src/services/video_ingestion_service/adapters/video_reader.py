from __future__ import annotations

import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class VideoReader:
    """OpenCV-based video source that yields frames sequentially."""

    def __init__(self, source_path: str) -> None:
        self._source_path = source_path
        self._cap: cv2.VideoCapture | None = None
        self._frame_count = 0
        self._fps: float = 0.0
        self._width: int = 0
        self._height: int = 0
        self._total_frames: int = 0

    def open(self) -> None:
        path = Path(self._source_path)
        if not path.exists():
            raise FileNotFoundError(f"Video source not found: {self._source_path}")

        self._cap = cv2.VideoCapture(str(path))
        if not self._cap.isOpened():
            raise RuntimeError(f"Failed to open video source: {self._source_path}")

        self._fps = self._cap.get(cv2.CAP_PROP_FPS) or 30.0
        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

        logger.info(
            "Opened video: %s (%dx%d, %.1f fps, %d frames)",
            self._source_path,
            self._width,
            self._height,
            self._fps,
            self._total_frames,
        )

    def read(self) -> Generator[tuple[int, np.ndarray], None, None]:
        """Yield ``(frame_number, ndarray)`` tuples until the source ends."""
        if self._cap is None:
            raise RuntimeError("VideoReader not opened — call open() first")

        while True:
            ret, frame = self._cap.read()
            if not ret:
                break
            self._frame_count += 1
            yield self._frame_count, frame

    def close(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
            logger.info("Video source closed (%d frames read)", self._frame_count)

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def total_frames(self) -> int:
        return self._total_frames
