const WS_BASE = import.meta.env.VITE_WS_BASE as string;

export function connectRtc(mapId: string, token: string, role: "viewer" | "device") {
  return new WebSocket(`${WS_BASE}/ws/rtc?map_id=${mapId}&token=${token}&role=${role}`);
}

export function connectControl(mapId: string, token: string, role: "viewer" | "device") {
  return new WebSocket(`${WS_BASE}/ws/control?map_id=${mapId}&token=${token}&role=${role}`);
}
