import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.deps import decode_token
from app.db.session import SessionLocal
from app.schemas.telemetry import TelemetryIn
from app.services.auth_service import get_map_if_allowed
from app.services.telemetry_service import save_telemetry
from app.ws.manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    token = ws.query_params.get("token")
    map_id = ws.query_params.get("map_id")

    if not token or not map_id:
        await ws.close(code=1008)
        return

    try:
        subject, subject_type = decode_token(token)

    except Exception:
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

            if subject_type != "device":
                continue

            data = json.loads(raw)
            msg = TelemetryIn(**data)  # dictionary key: value를 키워드 인자로 풀어서 전달

            if msg.map_id != map_id:
                continue

            async with SessionLocal() as db:
                await save_telemetry(db, map_obj.id, msg)

            await manager.broadcast(map_id, raw)

    except WebSocketDisconnect:
        manager.disconnect(map_id, ws)
