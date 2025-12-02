import cv2
import numpy as np
from .services.detector import detect_faces
from .services.embedder import compute_embedding_from_bgr

def extract_face(img_bgr):
    """
    Detects a single face, extracts & aligns it.
    Returns cropped face (BGR) or None.
    """
    detections = detect_faces(img_bgr)

    if not detections:
        return None
    
    # take the highest-confidence face
    det = max(detections, key=lambda x: x["score"])
    x, y, w, h = det["box"]

    # safety clamps
    h_img, w_img = img_bgr.shape[:2]
    x = max(0, x); y = max(0, y)
    x2 = min(x + w, w_img)
    y2 = min(y + h, h_img)

    face = img_bgr[y:y2, x:x2]

    if face is None or face.size == 0:
        return None
    
    return face

def extract_embedding(img_bgr):
    """
    Full pipeline:
    - detect face
    - crop
    - (optional) align
    - embed using ArcFace
    Returns: 512-d embedding list
    """
    face = extract_face(img_bgr)
    if face is None:
        return None

    embedding = compute_embedding_from_bgr(face)
    return embedding
