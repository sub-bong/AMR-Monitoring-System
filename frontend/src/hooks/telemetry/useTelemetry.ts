import { useEffect, useState } from "react";
import { connectTelemetryWS } from "../../services/ws";

export type Telemetry = {
  map_id: string;
  amr_id: string;
  pose: { x: number; y: number; yaw: number };
  state?: { battery_pct?: number; mode?: string; health?: string; speed_mps?: number };
};

export function useTelemetry(mapId: string, token: string) {
  const [telemetry, setTelemetry] = useState<Telemetry | null>(null);

  useEffect(() => {
    if (!mapId || !token) return;

    const ws = connectTelemetryWS(mapId, token);
    ws.onmessage = (ev) => {
      const data = JSON.parse(ev.data);
      setTelemetry(data);
    };
    ws.onclose = () => console.log("ws closed");
    ws.onerror = (e) => console.error("ws error", e);

    return () => ws.close();
  }, [mapId, token]);

  return telemetry;
}
