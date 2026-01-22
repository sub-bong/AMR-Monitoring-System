import { API_BASE } from "./api";

export async function listDevices(token: string) {
  const res = await fetch(`${API_BASE}/devices`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createDevice(token: string, name: string, map_id?: string) {
  const res = await fetch(`${API_BASE}/devices`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name, map_id }),
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function revokeDevice(token: string, deviceId: number) {
  const res = await fetch(`${API_BASE}/devices/${deviceId}/revoke`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
