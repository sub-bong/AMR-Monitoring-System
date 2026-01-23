import { useEffect } from "react";
import { connectControl } from "../../services/rtc";

export function useControlDevice(mapId: string, token: string, onCapture: () => void) {
  useEffect(() => {
    if (!mapId || !token) return;

    const ws = connectControl(mapId, token, "device");
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.type === "capture") onCapture();
    };

    return () => ws.close();
  }, [mapId, token, onCapture]);
}
