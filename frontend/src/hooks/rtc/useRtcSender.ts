import { useEffect } from "react";
import { connectRtc } from "../../services/rtc";

export function useRtcSender(mapId: string, token: string, getStream: () => MediaStream | null) {
  useEffect(() => {
    if (!mapId || !token) return;

    const ws = connectRtc(mapId, token, "device");
    const pc = new RTCPeerConnection({
      iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
    });

    ws.onopen = () => {
      ws.send(JSON.stringify({ type: "device-online" }));
    };

    const stream = getStream();
    if (stream) {
      stream.getTracks().forEach((t) => pc.addTrack(t, stream));
    }

    pc.onicecandidate = (e) => {
      if (e.candidate) ws.send(JSON.stringify({ type: "candidate", candidate: e.candidate }));
    };

    ws.onmessage = async (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.type === "offer") {
        await pc.setRemoteDescription({ type: "offer", sdp: msg.sdp });
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        ws.send(JSON.stringify({ type: "answer", sdp: answer.sdp }));
      }
      if (msg.type === "candidate") {
        await pc.addIceCandidate(msg.candidate);
      }
    };

    return () => {
      ws.close();
      pc.close();
    };
  }, [mapId, token, getStream]);
}
