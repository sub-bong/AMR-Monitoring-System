from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.deps import decode_token
from app.db.session import SessionLocal
from app.services.auth_service import get_map_if_allowed
from app.ws.room_manager import RoomManager

router = APIRouter()
manager = RoomManager()


@router.websocket("/ws/control")
async def ws_control(ws: WebSocket):
    token = ws.query_params.get("token")
    map_id = ws.query_params.get("map_id")
    role = ws.query_params.get("role")

    if not token or not map_id or role not in ("viewer", "device"):
        await ws.close(code=1008)
        return

    subject, subject_type = decode_token(token)
    if role == "viewer" and subject_type != "user":
        await ws.close(code=1008)
        return
    if role == "device" and subject_type != "device":
        await ws.close(code=1008)
        return

    async with SessionLocal() as db:
        map_obj = await get_map_if_allowed(db, map_id, subject_type, int(subject))
    if not map_obj:
        await ws.close(code=1008)
        return

    await manager.connect(map_id, ws)

    try:
        while True:
            raw = await ws.receive_text()
            await manager.broadcast(map_id, raw, sender=ws)
    except WebSocketDisconnect:
        manager.disconnect(map_id, ws)
