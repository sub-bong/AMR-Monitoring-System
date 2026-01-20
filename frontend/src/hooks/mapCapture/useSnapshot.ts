import { createSnapshot } from "../../services/snapshotApi";
import { blobToBase64 } from "../../utils/blob";
import type { Intrinsics, Pose, SnapshotPayload } from "../../types/snapshot";

export function useSnapshot(getCanvas: () => HTMLCanvasElement | null) {
  async function takeSnapshot(mapId: string, token: string) {
    if (!token) throw new Error("device token required");

    const canvas = getCanvas();

    if (!canvas) throw new Error("canvas not ready");

    const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob((b) => resolve(b), "image/jpeg", 0.9));
    if (!blob) throw new Error("failed to capture");

    const b64 = await blobToBase64(blob);

    const pose: Pose = { pos: [0, 0, 0], rot: [0, 0, 0, 1] };
    const intrinsics: Intrinsics = { fx: 500, fy: 500, cx: 320, cy: 240 };

    const payload: SnapshotPayload = {
      map_id: mapId,
      image_url: b64,
      pose,
      intrinsics,
      meta: { source: "webxr" },
    };

    return createSnapshot(payload, token);
  }

  return { takeSnapshot };
}
