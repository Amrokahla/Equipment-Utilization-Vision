from __future__ import annotations

import json
import logging

from confluent_kafka import Producer

logger = logging.getLogger(__name__)


class FrameProducer:
    """Kafka producer wrapper with delivery tracking."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self._topic = topic
        self._producer = Producer({
            "bootstrap.servers": bootstrap_servers,
            "linger.ms": 5,
            "batch.num.messages": 10,
            "queue.buffering.max.messages": 10000,
            "message.max.bytes": 10_485_760,
        })
        self._delivered = 0
        self._failed = 0

    def produce(self, message: dict) -> None:
        payload = json.dumps(message, default=str).encode("utf-8")
        self._producer.produce(
            self._topic,
            value=payload,
            callback=self._on_delivery,
        )
        self._producer.poll(0)

    def _on_delivery(self, err, msg) -> None:  # noqa: ANN001
        if err is not None:
            self._failed += 1
            logger.error("Delivery failed for topic=%s: %s", msg.topic(), err)
        else:
            self._delivered += 1

    def flush(self, timeout: float = 30.0) -> int:
        remaining = self._producer.flush(timeout)
        logger.info(
            "Producer flushed (delivered=%d, failed=%d, remaining=%d)",
            self._delivered, self._failed, remaining,
        )
        return remaining

    @property
    def delivered_count(self) -> int:
        return self._delivered

    @property
    def failed_count(self) -> int:
        return self._failed
