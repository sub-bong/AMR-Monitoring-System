export type Point = {
  x: number;
  y: number;
};

export function computeBBox(points: Point[]) {
  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  return { minX, maxX, minY, maxY, w: maxX - minX, h: maxY - minY };
}

export function mapToSvg(point: Point, bbox: ReturnType<typeof computeBBox>, size: number) {
  const padding = 20;
  const scale = Math.min((size - padding * 2) / bbox.w, (size - padding * 2) / bbox.h);
  const x = (point.x - bbox.minX) * scale + padding;
  const y = (bbox.maxY - point.y) * scale + padding; // y축 뒤집기

  return { x, y, scale };
}
