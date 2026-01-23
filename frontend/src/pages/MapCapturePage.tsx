import { useState } from "react";
import { ArViewport } from "../components/ArViewport";
import { CaptureControls } from "../components/CaptureControls";
import { useSnapshot } from "../hooks/mapCapture/useSnapshot";
import { useXrSession } from "../hooks/mapCapture/useXrSession";
import { useAuth } from "../hooks/auth/useAuth";
import { useRtcSender } from "../hooks/rtc/useRtcSender";
import { useControlDevice } from "../hooks/rtc/useControlDevice";

export default function MapCapturePage() {
  const [mapId, setMapId] = useState("map-001");
  const { deviceToken } = useAuth();

  const { mountRef, startSession, getCanvas, getXrMeta } = useXrSession();
  const { takeSnapshot } = useSnapshot(getCanvas, getXrMeta);

  // RTC 송신/제어 연결
  const stream = () => {
    const canvas = getCanvas();
    return canvas ? canvas.captureStream(20) : null;
  };

  useRtcSender(mapId, deviceToken, stream);
  useControlDevice(mapId, deviceToken, () => takeSnapshot(mapId, deviceToken));

  return (
    <div className="h-screen w-full">
      <ArViewport mountRef={mountRef} />
      <CaptureControls mapId={mapId} deviceToken={deviceToken} onMapIdChange={setMapId} onStart={startSession} onSnapshot={() => takeSnapshot(mapId, deviceToken)} />
    </div>
  );
}
