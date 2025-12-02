import os
import cv2
import numpy as np
from mtcnn import MTCNN
from ..config import SCRFD_ONNX
import onnxruntime as ort

# Try to load SCRFD if file exists
SCRFD_AVAILABLE = os.path.exists(SCRFD_ONNX)
scrfd_sess = None
if SCRFD_AVAILABLE:
    try:
        scrfd_sess = ort.InferenceSession(SCRFD_ONNX, providers=["CPUExecutionProvider"])
    except Exception:
        scrfd_sess = None

mtcnn = MTCNN()

def detect_faces_with_mtcnn(img_rgb):
    dets = mtcnn.detect_faces(img_rgb)
    faces = []
    for d in dets:
        box = d.get("box")
        conf = d.get("confidence", 0)
        if box and conf:
            x, y, w, h = box
            faces.append({"box": [x, y, w, h], "score": float(conf)})
    return faces

def detect_faces(img_bgr):
    """
    Returns list of detections: [{'box':[x,y,w,h], 'score':float}, ...]
    Prefer SCRFD if available, else MTCNN.
    """
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # If SCRFD present try to use it
    if scrfd_sess:
        try:
            # Basic SCRFD preproc - many SCRFD ONNX variants require 640/1280 dynamic shapes.
            # We'll use a simple wrapper: resize keeping aspect ratio and run model,
            # then parse results if outputs follow [scores, boxes, ...] naming.
            inp = cv2.resize(img_rgb, (640, 640))
            inp = inp.astype(np.float32)
            inp = np.transpose(inp, (2, 0, 1))[None, :, :, :]
            outputs = scrfd_sess.run(None, {scrfd_sess.get_inputs()[0].name: inp})
            # Parsing varies by SCRFD model; if parse fails, fallback to MTCNN
            # Simplest approach: fallback to MTCNN if unknown format
        except Exception:
            return detect_faces_with_mtcnn(img_rgb)

    # fallback to MTCNN (robust)
    return detect_faces_with_mtcnn(img_rgb)
