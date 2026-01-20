const WS_BASE = import.meta.env.VITE_WS_BASE as string;

export function connectTelemetryWS(mapId: string, token: string) {
  if (!WS_BASE) throw new Error("WS ENV 값이 비었습니다.");
  const url = `${WS_BASE}/ws/telemetry?map_id=${mapId}&token=${token}`;
  return new WebSocket(url);
}
