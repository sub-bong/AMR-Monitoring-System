import { API_BASE } from "./api";
import type { SnapshotPayload } from "../types/snapshot";

export async function createSnapshot(payload: SnapshotPayload, token: string) {
  const res = await fetch(`${API_BASE}/snapshots`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error(await res.text());

  return res.json();
}
