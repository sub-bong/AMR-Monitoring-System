type Props = {
  mapId: string;
  deviceToken: string;
  onMapIdChange: (v: string) => void;
  onTokenChange: (v: string) => void;
  onStart: () => void;
  onSnapshot: () => void;
};

export function CaptureControls({ mapId, deviceToken, onMapIdChange, onTokenChange, onStart, onSnapshot }: Props) {
  return (
    <div className="fixed bottom-4 left-4 right-4 flex gap-2 rounded-xl bg-white/80 p-3 shadow flex-wrap justify-end">
      <div className="flex flex-1 gap-2">
        <input
          className="text-slate-600 flex-1 rounded-lg border border-slate-100 focus:border-slate-400 focus:outline-none px-3 py-2"
          placeholder="Device Token"
          value={deviceToken}
          onChange={(e) => onTokenChange(e.target.value)}
        />
        <input
          className="text-slate-600 w-20 rounded-lg border border-slate-100 focus:border-slate-400 focus:outline-none px-3 py-2"
          placeholder="Map ID"
          value={mapId}
          onChange={(e) => onMapIdChange(e.target.value)}
        />
      </div>
      <div className="flex gap-2">
        <button className="cursor-pointer rounded-lg bg-black px-4 py-2 text-white" onClick={onStart}>
          Start AR
        </button>
        <button className="cursor-pointer rounded-lg bg-blue-600 px-4 py-2 text-white" onClick={onSnapshot}>
          Snapshot
        </button>
      </div>
    </div>
  );
}
