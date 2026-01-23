import { useState } from "react";
import { useAuth } from "../hooks/auth/useAuth";
import { useRtcViewer } from "../hooks/rtc/useRtcViewer";
import { connectControl } from "../services/rtc";

export default function RemoteViewerPage() {
  const { userToken } = useAuth();
  const [mapId, setMapId] = useState("map-001");

  const { videoRef } = useRtcViewer(mapId, userToken);

  function sendCapture() {
    if (!userToken) return;
    const ws = connectControl(mapId, userToken, "viewer");
    ws.onopen = () => {
      ws.send(JSON.stringify({ type: "capture" }));
      ws.close();
    };
  }

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="mb-4 text-xl font-semibold">Remote Viewer</h1>
      <div className="mb-4 flex gap-2">
        <input className="rounded border px-3 py-2 text-slate-600" value={mapId} onChange={(e) => setMapId(e.target.value)} />
        <button className="rounded bg-blue-600 px-4 py-2 text-white" onClick={sendCapture}>
          원격 촬영
        </button>
      </div>
      <video ref={videoRef} autoPlay playsInline className="w-full rounded-lg bg-black" />
    </div>
  );
}
