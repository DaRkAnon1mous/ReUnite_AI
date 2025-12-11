# pipeline.py
import cv2
import numpy as np
from .services.detector import detect_faces
from .services.embedder import compute_embedding_from_bgr

def extract_face(img_bgr):
    """
    Extract face from image. Handles both full images and pre-cropped faces.
    """
    h, w = img_bgr.shape[:2]
    
    # If already a face crop, return as-is
    if h <= 300 and w <= 300 and abs(h - w) < 50:
        print(f"⚡ Image is {h}x{w}, treating as pre-cropped face")
        return img_bgr
    
    # Otherwise detect
    detections = detect_faces(img_bgr, score_thresh=0.3)
    print(f"🔍 Found {len(detections)} faces")

    if not detections:
        # Fallback for small images
        if h < 400 and w < 400:
            print(f"⚠️ No detection but image is small, using as-is")
            return img_bgr
        return None
    
    det = max(detections, key=lambda x: x["score"])
    x, y, w, h = det["box"]

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
    Full pipeline: extract face → embed
    """
    face = extract_face(img_bgr)
    if face is None:
        return None

    embedding = compute_embedding_from_bgr(face)
    return embedding