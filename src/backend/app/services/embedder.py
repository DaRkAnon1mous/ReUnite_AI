import onnxruntime as ort
import numpy as np
import cv2
from ..config import BUFFALO_ONNX as ARC_PATH

# initialize ONNX session once
session = ort.InferenceSession(ARC_PATH, providers=["CPUExecutionProvider"])

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def preprocess_face_bgr(img_bgr):
    # ArcFace expects 112x112, normalized as (img - 127.5)/128
    img = cv2.resize(img_bgr, (112, 112))
    # convert BGR->RGB for model if it expects RGB; our earlier model used RGB normalization
    img = img[:, :, ::-1]
    img = np.transpose(img, (2, 0, 1)).astype(np.float32)
    img = np.expand_dims(img, axis=0)
    img = (img - 127.5) / 128.0
    return img

def compute_embedding_from_bgr(img_bgr):
    x = preprocess_face_bgr(img_bgr)
    embedding = session.run([output_name], {input_name: x})[0][0]
    # L2 normalize
    embedding = embedding / np.linalg.norm(embedding)# Normalize to make cosine similarity meaningful
    return embedding.tolist()
