import { useEffect, useState } from "react";
import { useAuth } from "../hooks/auth/useAuth";
import { createDevice, listDevices, revokeDevice } from "../services/deviceApi";
import { apiGet } from "../services/api";

type Device = { id: number; name: string; is_active: boolean };

export default function DeviceAdminPage() {
  const { userToken } = useAuth();
  const [items, setItems] = useState<Device[]>([]);
  const [name, setName] = useState("");
  const [mapId, setMapId] = useState("");
  const [issuedKey, setIssuedKey] = useState("");
  const [error, setError] = useState("");

  async function load() {
    if (!userToken) return;
    const res = await listDevices(userToken);
    setItems(res.items);
  }

  useEffect(() => {
    let active = true;

    (async () => {
      const res = await apiGet<{ ok: boolean; items: Device[] }>("/devices", userToken);
      if (active) setItems(res.items);
    })();

    return () => {
      active = false;
    };
  }, [userToken]);

  async function handleCreate() {
    try {
      setError("");
      const res = await createDevice(userToken, name, mapId || undefined);
      setIssuedKey(res.device_key);
      setName("");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "create failed");
    }
  }

  async function handleRevoke(id: number) {
    await revokeDevice(userToken, id);
    await load();
  }

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <h1 className="mb-6 text-2xl font-semibold">Device 관리</h1>

      {error && <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      <div className="mb-6 rounded-xl border bg-white/70 p-4">
        <div className="flex gap-2">
          <input className="flex-1 rounded border px-3 py-2 text-slate-600" placeholder="Device 이름" value={name} onChange={(e) => setName(e.target.value)} />
          <input className="w-40 rounded border px-3 py-2 text-slate-600" placeholder="Map ID (옵션)" value={mapId} onChange={(e) => setMapId(e.target.value)} />
          <button className="rounded bg-slate-900 px-4 py-2 text-white" onClick={handleCreate}>
            생성
          </button>
        </div>
        {issuedKey && <div className="mt-2 text-sm text-slate-600">발급 키(1회): {issuedKey}</div>}
      </div>

      <div className="space-y-2">
        {items.map((d) => (
          <div key={d.id} className="flex items-center justify-between rounded border bg-white/70 px-4 py-2 text-slate-600">
            <div>
              {d.id} / {d.name} / {d.is_active ? "active" : "revoked"}
            </div>
            {d.is_active && (
              <button className="rounded bg-rose-500 px-3 py-1 text-white" onClick={() => handleRevoke(d.id)}>
                revoke
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
