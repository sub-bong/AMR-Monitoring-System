import { createSnapshot } from "../../services/snapshotApi";
import { blobToBase64 } from "../../utils/blob";
import type { SnapshotPayload } from "../../types/snapshot";

export function useSnapshot(
  getCanvas: () => HTMLCanvasElement | null,
  getXrMeta: () => {
    pose: { pos: number[]; rot: number[] };
    intrinsics: { fx: number; fy: number; cx: number; cy: number };
    projection: number[];
    viewport: { w: number; h: number };
  } | null,
) {
  async function takeSnapshot(mapId: string, token: string) {
    if (!token) throw new Error("device token required");

    const canvas = getCanvas();

    if (!canvas) throw new Error("canvas not ready");

    const xr = getXrMeta();
    if (!xr) throw new Error("XR pose not ready");

    const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob((b) => resolve(b), "image/jpeg", 0.9));
    if (!blob) throw new Error("failed to capture");

    const b64 = await blobToBase64(blob);

    const payload: SnapshotPayload = {
      map_id: mapId,
      image_url: b64,
      pose: xr.pose,
      intrinsics: xr.intrinsics,
      meta: {
        source: "webxr",
        projection: xr.projection,
        viewport: xr.viewport,
      },
    };

    return createSnapshot(payload, token);
  }

  return { takeSnapshot };
}
