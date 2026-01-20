import type { Point } from "../utils/coords";
import { computeBBox, mapToSvg } from "../utils/coords";

type Props = {
  polygon: Point[];
  amr?: Point;
};

export function MapCanvas({ polygon, amr }: Props) {
  if (!polygon.length) return <div className="rounded-2xl border border-slate-300 bg-white/60 p-8 text-sm text-slate-500">No map</div>;

  const size = 500;
  const bbox = computeBBox(polygon);

  const polyPoints = polygon
    .map((p) => {
      const { x, y } = mapToSvg(p, bbox, size);
      return `${x}, ${y}`;
    })
    .join(" ");

  const amrPt = amr ? mapToSvg(amr, bbox, size) : null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white/70 p-4 shadow-sm">
      <svg width={size} height={size} className="rounded-xl bg-slate-50">
        <polygon points={polyPoints} fill="rgba(100,150,240,0.2" stroke="#2b6cb0" strokeWidth={2} />
        {amrPt && <circle cx={amrPt.x} cy={amrPt.y} r={6} fill="#e53e3e" />}
      </svg>
    </div>
  );
}
