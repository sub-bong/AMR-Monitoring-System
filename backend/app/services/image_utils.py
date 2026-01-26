import base64
import cv2
import numpy as np


def decode_data_url(data_url: str):
    header, b64 = data_url.split(",", 1)
    raw = base64.b64decode(b64)
    img = np.frombuffer(raw, dtype=np.uint8)

    return cv2.imdecode(img, cv2.IMREAD_COLOR)
