import { useEffect, useState } from "react";
import { MapCanvas } from "./components/MapCanvas";
import { apiGet } from "./services/api";
import { useTelemetry } from "./hooks/telemetry/useTelemetry";

type Point = { x: number; y: number };

export default function App() {
  const [userToken, setUserToken] = useState("");
  const [mapId, setMapId] = useState("map-001");
  const [polygon, setPolygon] = useState<Point[]>([]);
  const [deviceToken, setDeviceToken] = useState("");

  const telemetry = useTelemetry(mapId, deviceToken);

  async function loadMap() {
    const res = await apiGet<{ ok: boolean; map: { polygon: Point[] } }>(`/maps/${mapId}`, userToken);
    setPolygon(res.map.polygon);
  }

  useEffect(() => {
    if (!userToken || !mapId) return;

    let active = true;
    (async () => {
      const res = await apiGet<{ ok: boolean; map: { polygon: Point[] } }>(`/maps/${mapId}`, userToken);
      if (active) setPolygon(res.map.polygon);
    })();

    return () => {
      active = false;
    };
  }, [userToken, mapId]);

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-50 via-white to-slate-100 text-slate-900">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-8">
          <h1 className="text-2xl font-semibold tracking-tight">AMR Monitoring</h1>
          <p className="text-sm text-slate-500">실시간 Map</p>
        </header>

        <div className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
          <section className="space-y-4">
            <div className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm">
              <div className="grid gap-4">
                <label className="text-xs uppercase tracking-[0.2em] text-slate-500">User Token</label>
                <input
                  className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none"
                  value={userToken}
                  onChange={(e) => setUserToken(e.target.value)}
                />

                <label className="text-xs uppercase tracking-[0.2em] text-slate-500">Device Token</label>
                <input
                  className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none"
                  value={deviceToken}
                  onChange={(e) => setDeviceToken(e.target.value)}
                />

                <div className="flex flex-wrap items-center gap-3">
                  <div className="flex-1">
                    <label className="text-xs uppercase tracking-[0.2em] text-slate-500"></label>
                    <input
                      className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none"
                      value={mapId}
                      onChange={(e) => setMapId(e.target.value)}
                    />
                  </div>
                  <button className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800" onClick={loadMap}>
                    Load Map
                  </button>
                </div>
              </div>
            </div>

            <MapCanvas polygon={polygon} amr={telemetry ? { x: telemetry.pose.x, y: telemetry.pose.y } : undefined} />
          </section>

          <aside className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm">
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Telemetry</h3>
            <div className="rounded-xl bg-slate-900/90 p-4 text-xs text-slate-100">
              <pre className="whitespace-pre-wrap">{JSON.stringify(telemetry, null, 2)}</pre>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
