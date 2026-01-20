export function projectionToIntrinsics(proj: number[], width: number, height: number) {
  const fx = (proj[0] * width) / 2;
  const fy = (proj[5] * height) / 2;
  const cx = ((1 - proj[8]) * width) / 2;
  const cy = ((1 + proj[9]) * height) / 2;
  return { fx, fy, cx, cy };
}
