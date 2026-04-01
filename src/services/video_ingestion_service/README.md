# `video_ingestion_service`

The Video Ingestion Service is the **first producer** in the Eaglevision pipeline. It reads a video source, encodes frames as JPEG, and publishes them to the `raw_frames` Kafka topic for downstream CV processing.

## What it does

1. Opens a video file (path from `VIDEO_SOURCE_PATH`)
2. Reads frames sequentially, applying stride and JPEG encoding
3. Publishes each frame as a JSON message to `raw_frames`
4. Logs heartbeat counters and shuts down gracefully on SIGTERM/SIGINT

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` | Kafka broker address |
| `KAFKA_RAW_FRAMES_TOPIC` | `raw_frames` | Target Kafka topic |
| `VIDEO_SOURCE_PATH` | `/data/demo.mp4` | Path to video file inside the container |
| `SOURCE_ID` | *(derived from filename)* | Logical identifier for the video source |
| `FRAME_STRIDE` | `1` | Publish every Nth frame (1 = every frame) |
| `JPEG_QUALITY` | `80` | JPEG compression quality (0–100) |
| `INGEST_LOOP_SLEEP_MS` | `0` | Optional delay between frames (ms) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Running

Place a video file in the project `data/` directory, then:

```bash
make dev    # starts all backend services including video-ingestion
```

The service expects the video at the path configured by `VIDEO_SOURCE_PATH` (default `/data/demo.mp4`). The `data/` directory is mounted into the container as `/data/`.
