from typing import Dict, Set
from fastapi import WebSocket


class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(room, set()).add(ws)

    def disconnect(self, room: str, ws: WebSocket):
        if room in self.rooms:
            self.rooms[room].discard(ws)
            if not self.rooms[room]:
                self.rooms.pop(room, None)

    async def broadcast(self, room: str, message: str, sender: WebSocket | None = None):
        for ws in list(self.rooms.get(room, set())):
            if sender is not None and ws is sender:
                continue
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(room, ws)
