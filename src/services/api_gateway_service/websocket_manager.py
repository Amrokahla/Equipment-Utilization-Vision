from __future__ import annotations

import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Track connected WebSocket clients and broadcast messages to all."""

    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._clients.add(websocket)
        logger.info("WebSocket client connected (%d total)", len(self._clients))

    def disconnect(self, websocket: WebSocket) -> None:
        self._clients.discard(websocket)
        logger.info("WebSocket client disconnected (%d remaining)", len(self._clients))

    async def broadcast(self, message: str) -> None:
        """Send *message* to every connected client, pruning stale ones."""
        stale: set[WebSocket] = set()
        for client in self._clients:
            try:
                await client.send_text(message)
            except Exception:
                stale.add(client)
        if stale:
            self._clients -= stale
            logger.info("Removed %d stale WebSocket clients", len(stale))

    @property
    def client_count(self) -> int:
        return len(self._clients)
