from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "kafka:29092"
    kafka_raw_frames_topic: str = "raw_frames"

    video_source_path: str = "/data/demo.mp4"
    source_id: str = ""
    frame_stride: int = 1
    max_queue_size: int = 200
    jpeg_quality: int = 80
    ingest_loop_sleep_ms: int = 0
    log_level: str = "INFO"

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
