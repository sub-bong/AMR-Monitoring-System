export type Pose = {
  pos: number[];
  rot: number[];
};

export type Intrinsics = {
  fx: number;
  fy: number;
  cx: number;
  cy: number;
};

export type SnapshotPayload = {
  map_id: string;
  image_url: string;
  pose: Pose;
  intrinsics: Intrinsics;
  meta?: Record<string, unknown>;
};
