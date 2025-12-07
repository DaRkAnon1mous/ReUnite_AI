# 📘 TECH_STACK.md


# Tech Stack – ReUnite AI

## Frontend
- **React (Vite)**
- TailwindCSS
- Clerk Auth
- DaisyUI / ShadCN Components
- Axios

## Backend
- **FastAPI**
- ONNXRuntime (CPU inference)
- ArcFace glintr100 (embedding)
- SCRFD 2.5g ONNX (face detection)
- PostgreSQL with SQLAlchemy ORM
- Redis (Upstash) for caching
- Cloudinary for image uploads

## Vector Database
- **Qdrant Cloud**
  - Collection: `faces_collection`
  - 512-dim vectors
  - Cosine distance

## Deployment
- **Backend** → HuggingFace Spaces (Docker)
- **Frontend** → Netlify
- **PostgreSQL** → NeonDB
- **Redis** → Upstash
```

