import { Link } from "react-router-dom";

type Props = {
  mapId: string;
  deviceToken: string;
  onMapIdChange: (v: string) => void;
  onStart: () => void;
  onSnapshot: () => void;
};

export function CaptureControls({ mapId, deviceToken, onMapIdChange, onStart, onSnapshot }: Props) {
  const tokenReady = Boolean(deviceToken);

  return (
    <div className="fixed bottom-4 left-4 right-4 flex gap-2 rounded-xl bg-white/80 p-3 shadow flex-wrap justify-end">
      <div className="flex gap-2">
        <input className="text-slate-600 flex-1 rounded-lg border px-3 py-2" placeholder="Map ID" value={mapId} onChange={(e) => onMapIdChange(e.target.value)} />

        <div className="flex items-center gap-2 text-xs">
          <span className="text-slate-600">Device Token</span>
          <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${tokenReady ? "bg-emerald-100 text-emerald-700" : "bg-rose-100 text-rose-700"}`}>
            {tokenReady ? "설정됨" : "없음"}
          </span>
          {!tokenReady && (
            <Link className="text-slate-600 underline" to="/auth">
              발급하기
            </Link>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <button className="cursor-pointer rounded-lg bg-black px-4 py-2 text-white" onClick={onStart}>
          Start AR
        </button>
        <button className="cursor-pointer rounded-lg bg-blue-600 px-4 py-2 text-white" onClick={onSnapshot} disabled={!tokenReady}>
          Snapshot
        </button>
      </div>
    </div>
  );
}
