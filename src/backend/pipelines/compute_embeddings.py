import cv2
import numpy as np
# from keras_facenet import FaceNet
import onnxruntime as ort

session = ort.InferenceSession("src/backend/models/model.onnx")

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def preprocess_face(img):
    # ArcFace expects 112x112 RGB, normalized
    img = cv2.resize(img, (112, 112))
    img = img[:, :, ::-1]  # BGR → RGB
    img = np.transpose(img, (2, 0, 1))  # HWC → CHW
    img = np.expand_dims(img, axis=0).astype(np.float32)
    img = (img - 127.5) / 128.0
    return img

def compute_embedding(image_path):
    img_bgr  = cv2.imread(image_path)
    if img_bgr  is None:
        return None
    
    # FaceNet expects RGB
    img = preprocess_face(img_bgr)
    
    # face = cv2.resize(img, (160,160))

    # Detect + embed
    embedding=session.run([output_name], {input_name: img})[0][0]# Run ONNX inference


    # L2 normalization
    embedding = embedding / np.linalg.norm(embedding)

    # Return 128-d vector
    return embedding.tolist()
