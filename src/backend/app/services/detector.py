import cv2
import numpy as np
import onnxruntime as ort
from ..config import SCRFD_ONNX

# Load ONNX session once
session = ort.InferenceSession(SCRFD_ONNX, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

def detect_faces(img_bgr):
    """
    Returns list of detections: [{"box": [x,y,w,h], "score": float}]
    """

    h, w = img_bgr.shape[:2]

    # Preprocess
    img = cv2.resize(img_bgr, (640, 640))
    img = img[:, :, ::-1]  # BGR → RGB
    img = img.astype(np.float32)
    img /= 255.0
    img = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)

    outputs = session.run(None, {input_name: img})

    # SCRFD gives output: scores, bboxes
    scores = outputs[0][0]
    bboxes = outputs[1][0]

    detections = []
    for score, box in zip(scores, bboxes):
        if score < 0.3:  # threshold
            continue

        x1, y1, x2, y2 = box
        x1 = int(x1 * w / 640)
        y1 = int(y1 * h / 640)
        x2 = int(x2 * w / 640)
        y2 = int(y2 * h / 640)

        detections.append({
            "box": [x1, y1, x2 - x1, y2 - y1],
            "score": float(score)
        })

    return detections
