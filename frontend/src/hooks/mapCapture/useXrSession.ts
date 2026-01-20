import { useEffect, useRef, useState } from "react";
import * as THREE from "three";

export function useXrSession() {
  const mountRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sessionRef = useRef<XRSession | null>(null);

  const [requested, setRequested] = useState(false);

  useEffect(() => {
    if (!requested) return;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.xr.enabled = true;

    if (mountRef.current) {
      mountRef.current.innerHTML = "";
      mountRef.current.appendChild(renderer.domElement);
    }

    rendererRef.current = renderer;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera();

    let cancelled = false;

    (async () => {
      /* eslint-disable @typescript-eslint/no-explicit-any */

      if (!(navigator as any).xr) {
        alert("WebXR을 자원하지 않습니다.");
        return;
      }

      const supported = await (navigator as any).xr.isSessionSupported("immersive-ar");
      if (!supported) {
        alert("immersive-ar을 지원하지 않는 디바이스/브라우저 입니다.");
        return;
      }
      try {
        const session = await (navigator as any).xr.requestSession("immersive-ar", {
          requiredFeatures: ["hit-test"],
        });
        if (cancelled) {
          await session.end();
          return;
        }
        sessionRef.current = session;
        renderer.xr.setSession(session);
        renderer.setAnimationLoop(() => renderer.render(scene, camera));
      } catch (e) {
        console.error(e);
        alert("AR 세션 시작을 실패하였습니다.");
      }
    })();

    return () => {
      cancelled = true;
      sessionRef.current?.end();
      sessionRef.current = null;
      renderer.setAnimationLoop(null);
      renderer.dispose();
      rendererRef.current = null;
    };
  }, [requested]);

  const startSession = () => setRequested(true);
  const getCanvas = () => rendererRef.current?.domElement ?? null;

  return { mountRef, startSession, getCanvas };
}
