from __future__ import annotations

import asyncio
import json
import logging
import threading
from datetime import datetime, timezone

from confluent_kafka import Consumer, KafkaError, KafkaException

from .websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)

TOPIC_TO_WS_TYPE: dict[str, str] = {
    "machine_events": "machine_event",
    "machine_state": "machine_state",
    "analytics_updates": "analytics_update",
}


class KafkaConsumerManager:
    """Threaded Kafka consumer that forwards messages to WebSocket clients.

    Runs confluent-kafka's synchronous poll loop in a daemon thread and
    pushes received messages into the asyncio event loop via
    ``run_coroutine_threadsafe``.
    """

    def __init__(self, bootstrap_servers: str, ws_manager: WebSocketManager) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._ws_manager = ws_manager
        self._running = False
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    # -- lifecycle ----------------------------------------------------------

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        self._running = True
        self._loop = loop
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="kafka-consumer"
        )
        self._thread.start()
        logger.info("Kafka consumer thread started")

    def stop(self) -> None:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10)
        logger.info("Kafka consumer thread stopped")

    @property
    def is_running(self) -> bool:
        return (
            self._running
            and self._thread is not None
            and self._thread.is_alive()
        )

    # -- internal -----------------------------------------------------------

    def _run(self) -> None:
        conf = {
            "bootstrap.servers": self._bootstrap_servers,
            "group.id": "eaglevision-gateway",
            "auto.offset.reset": "latest",
            "enable.auto.commit": True,
        }

        consumer: Consumer | None = None
        try:
            consumer = Consumer(conf)
            topics = list(TOPIC_TO_WS_TYPE.keys())
            consumer.subscribe(topics)
            logger.info("Subscribed to Kafka topics: %s", topics)

            while self._running:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error("Kafka consumer error: %s", msg.error())
                    continue

                self._handle_message(msg)
        except KafkaException:
            logger.exception("Kafka consumer fatal error")
        finally:
            if consumer is not None:
                consumer.close()

    def _handle_message(self, msg) -> None:  # noqa: ANN001
        try:
            value = msg.value()
            if value is None:
                return

            payload = json.loads(value.decode("utf-8"))
            ws_type = TOPIC_TO_WS_TYPE.get(msg.topic(), "unknown")
            envelope = {
                "type": ws_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "payload": payload,
            }
            message_text = json.dumps(envelope, default=str)

            if self._loop and not self._loop.is_closed():
                asyncio.run_coroutine_threadsafe(
                    self._ws_manager.broadcast(message_text),
                    self._loop,
                )
        except Exception:
            logger.exception(
                "Failed to process Kafka message from topic=%s", msg.topic()
            )
