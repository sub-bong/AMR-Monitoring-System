from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, map_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self.rooms.setdefault(map_id, set()).add(ws)

    def disconnect(self, map_id: str, ws: WebSocket) -> None:
        if map_id in self.rooms:
            self.rooms[map_id].discard(ws)

            if not self.rooms[map_id]:
                self.rooms.pop(map_id, None)

    async def broadcast(self, map_id: str, message: str) -> None:
        for ws in list(self.rooms.get(map_id, set())):
            try:
                await ws.send_text(message)

            except Exception:
                self.disconnect(map_id, ws)
