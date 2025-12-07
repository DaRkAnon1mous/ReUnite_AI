# AI Models Used in ReUnite AI

---

## 1️⃣ SCRFD 2.5g ONNX (Face Detector)

### Purpose:
Detect faces in images, return bounding boxes + landmarks.

### Why this model?
- Lightweight
- High accuracy
- CPU-friendly
- Works perfectly on HuggingFace Spaces free tier

### Output:
- Bounding box
- 5 facial landmarks
- Detection score

---

## 2️⃣ ArcFace – glintr100 (Face Embeddings)

### Purpose:
Convert a face into a **512-dimensional identity vector**.

### Why glintr100?
- Extremely accurate
- Robust to age, pose, lighting
- Perfect for missing person search
- ONNXRuntime compatible

### Embedding process:
```

face → resize → normalize → forward pass → 512D vector → L2 normalize

```

---

## 3️⃣ Qdrant Vector Search Engine

### Purpose:
Store and retrieve face embeddings using nearest-neighbour search.

### Why Qdrant?
- Cloud hosted (free tier available)
- High performance
- Supports cosine similarity
- Payload indexing (verified users)

### Collection structure:
- vector: 512 floats
- payload:
  - person_id
  - image_url
  - verified
```
