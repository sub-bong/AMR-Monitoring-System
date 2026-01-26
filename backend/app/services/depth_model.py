import os
import torch

# model path
DEPTH_WEIGHTS = os.getenv("DEPTH_ANYTHING_WEIGHTS",
                          "models/depth_anything_v2.pth")

_model = None


def load_depth_model():
    global _model
    if _model is not None:
        return _model

    from depth_anything_v2.dpt import DepthAnythingV2

    model = DepthAnythingV2(encoder="vitl")
    model.load_state_dict(torch.load(DEPTH_WEIGHTS, map_location="cpu"))
    model.eval()

    _model = model
    return _model


@torch.no_grad()
def infer_depth(model, image_bgr):
    import cv2
    import numpy as np

    img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0

    # Depth Anything V2의 입력 전처리에 맞게 조정 필요
    inp = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)

    depth = model(inp)  # shape -> [1, H, W] or [H, W]
    if depth.ndim == 3:
        depth = depth[0]
    depth = depth.cpu().numpy()
    return depth
