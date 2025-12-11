# src/backend/app/services/detector.py

import cv2
import numpy as np
import onnxruntime as ort
from ..config import SCRFD_ONNX


session = ort.InferenceSession(SCRFD_ONNX, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

STRIDES = [8, 16, 32]
NUM_ANCHORS = 2  # SCRFD uses 2 anchors per location


def preprocess(img, size=640):
    img_resized = cv2.resize(img, (size, size))
    blob = img_resized.astype(np.float32)
    blob = blob.transpose(2, 0, 1)[None, ...]
    return blob, img_resized.shape[:2]


def generate_anchors(feat_shape, stride):
    # centers of each cell in feature map
    h, w = feat_shape
    anchor_centers = []
    for i in range(h):
        for j in range(w):
            cx = (j + 0.5) * stride
            cy = (i + 0.5) * stride
            anchor_centers.append([cx, cy])
    anchor_centers = np.array(anchor_centers)
    anchor_centers = np.repeat(anchor_centers, NUM_ANCHORS, axis=0)
    return anchor_centers


def decode_bboxes(anchors, preds):
    # SCRFD bbox format: dx, dy, dw, dh (all scaled by stride)
    x = anchors[:, 0]
    y = anchors[:, 1]

    dx = preds[:, 0]
    dy = preds[:, 1]
    dw = preds[:, 2]
    dh = preds[:, 3]

    x1 = x - dx
    y1 = y - dy
    x2 = x + dw
    y2 = y + dh

    return np.stack([x1, y1, x2, y2], axis=-1)


def nms(boxes, scores, thresh=0.4):
    x1, y1, x2, y2 = boxes.T
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep = []

    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)

        inter = w * h
        iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-9)

        inds = np.where(iou <= thresh)[0]
        order = order[inds + 1]

    return keep


def detect_faces(img_bgr, score_thresh=0.4, size=640):
    h0, w0 = img_bgr.shape[:2]
    blob, _ = preprocess(img_bgr, size)

    outputs = session.run(None, {input_name: blob})

    all_scores = []
    all_boxes = []

    idx = 0
    for stride in STRIDES:
        # shapes: (N,1), (N,4)
        scores = outputs[idx].reshape(-1)
        bboxes = outputs[idx + 3].reshape(-1, 4)

        h_feat = size // stride
        w_feat = size // stride

        anchors = generate_anchors((h_feat, w_feat), stride)

        # decode box deltas
        bboxes = decode_bboxes(anchors, bboxes)

        # filter low scores
        mask = scores > score_thresh
        scores = scores[mask]
        bboxes = bboxes[mask]

        all_scores.append(scores)
        all_boxes.append(bboxes)

        idx += 1

    if len(all_scores) == 0:
        return []

    scores = np.concatenate(all_scores, axis=0)
    boxes = np.concatenate(all_boxes, axis=0)

    # scale back to original
    scale_x = w0 / size
    scale_y = h0 / size
    boxes[:, [0, 2]] *= scale_x
    boxes[:, [1, 3]] *= scale_y

    # NMS
    keep = nms(boxes, scores, thresh=0.45)

    detections = []
    for i in keep:
        x1, y1, x2, y2 = boxes[i]
        x1 = int(max(0, x1))
        y1 = int(max(0, y1))
        x2 = int(min(w0, x2))
        y2 = int(min(h0, y2))
        detections.append({
            "box": [x1, y1, x2 - x1, y2 - y1],
            "score": float(scores[i])
        })

    return detections
