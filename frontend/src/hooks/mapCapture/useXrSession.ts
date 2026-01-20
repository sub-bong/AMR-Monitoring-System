import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { projectionToIntrinsics } from "../../utils/projectionToIntrinsics";

type XrMeta = {
  pose: { pos: number[]; rot: number[] };
  intrinsics: { fx: number; fy: number; cx: number; cy: number };
  projection: number[];
  viewport: { w: number; h: number };
};

export function useXrSession() {
  const mountRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sessionRef = useRef<XRSession | null>(null);
  const refSpaceRef = useRef<XRReferenceSpace | null>(null);
  const lastMetaRef = useRef<XrMeta | null>(null);

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
        setRequested(false);
        return;
      }

      const supported = await (navigator as any).xr.isSessionSupported("immersive-ar");
      if (!supported) {
        alert("immersive-ar을 지원하지 않는 디바이스/브라우저 입니다.");
        setRequested(false);
        return;
      }
      const session = await (navigator as any).xr.requestSession("immersive-ar", {
        optionalFeatures: ["hit-test"], // 지원기기 호환을 위해 requiredFeatures -> optionalFeatures로 변경
      });
      if (cancelled) {
        await session.end();
        return;
      }
      sessionRef.current = session;
      refSpaceRef.current = await session.requestReferenceSpace("local");
      renderer.xr.setSession(session);

      renderer.setAnimationLoop((_, frame) => {
        if (!frame || !refSpaceRef.current || !sessionRef.current) {
          renderer.render(scene, camera);
          return;
        }
        const pose = frame.getViewerPose(refSpaceRef.current);
        if (pose) {
          const view = pose.views[0];
          const { position, orientation } = view.transform;

          const layer = sessionRef.current.renderState.baseLayer;

          if (layer) {
            const viewport = layer.getViewport(view);
            if (!viewport) {
              renderer.render(scene, camera);
              return;
            }

            const proj = Array.from(view.projectionMatrix);
            const intrinsics = projectionToIntrinsics(proj, viewport.width, viewport.height);

            lastMetaRef.current = {
              pose: {
                pos: [position.x, position.y, position.z],
                rot: [orientation.x, orientation.y, orientation.z, orientation.w],
              },
              intrinsics,
              projection: proj,
              viewport: { w: viewport?.width, h: viewport?.height },
            };
          }
        }

        renderer.render(scene, camera);
      });
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
  const getXrMeta = () => lastMetaRef.current;

  return { mountRef, startSession, getCanvas, getXrMeta };
}
