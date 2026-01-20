import type { RefObject } from "react";

export function ArViewport({ mountRef }: { mountRef: RefObject<HTMLDivElement | null> }) {
  return <div ref={mountRef} className="fixed inset-0 mt-20 mb-20" />;
}
