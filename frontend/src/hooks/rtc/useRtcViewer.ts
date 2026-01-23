import { useEffect, useRef } from "react";
import { connectRtc } from "../../services/rtc";

export function useRtcViewer(mapId: string, token: string) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (!mapId || !token) return;

    const ws = connectRtc(mapId, token, "viewer");
    const pc = new RTCPeerConnection({
      iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
    });

    pc.ontrack = (e) => {
      if (videoRef.current) videoRef.current.srcObject = e.streams[0];
    };

    pc.onicecandidate = (e) => {
      if (e.candidate) ws.send(JSON.stringify({ type: "candidate", candidate: e.candidate }));
    };

    ws.onmessage = async (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.type === "device-online") {
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        ws.send(JSON.stringify({ type: "offer", sdp: offer.sdp }));
      }
      if (msg.type === "answer") {
        await pc.setRemoteDescription({ type: "answer", sdp: msg.sdp });
      }
      if (msg.type === "candidate") {
        await pc.addIceCandidate(msg.candidate);
      }
    };

    return () => {
      ws.close();
      pc.close();
    };
  }, [mapId, token]);

  return { videoRef };
}
