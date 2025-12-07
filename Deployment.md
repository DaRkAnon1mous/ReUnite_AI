# Deployment Guide – ReUnite AI

This document contains step-by-step instructions to deploy the backend to **Hugging Face Spaces** and the frontend to **Netlify**.

---

# 🟦 Backend Deployment – Hugging Face Spaces (Docker)

### 1. Create a new Space:
- Space type → **Docker**
- Hardware → **CPU Basic**
- Visibility → Public

### 2. In your repository root, ensure:
- `Dockerfile` exists
- `requirements_backend.txt` exists
- Backend code is inside `/src/backend`

### 3. Add **secrets** in the HF Space settings:
````

NEON_DB_URL=
QDRANT_URL=
QDRANT_API_KEY=
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLERK_ISSUER=
CLERK_AUD=
ADMIN_EMAIL=

````

> Use **“Repository Secrets”** → these remain private.

### 4. Push your project → HuggingFace builds automatically.

### 5. Test backend:
```

[https://huggingface.co/spaces/USERNAME/SPACE_NAME](https://huggingface.co/spaces/USERNAME/SPACE_NAME)

```

---

# 🟩 Frontend Deployment – Netlify (React + Vite)

### 1. Upload frontend folder:
Upload only:
```

src/frontend/reunite-frontend

```

### 2. Netlify settings:
**Build Command**
```

npm run build

```

**Publish Directory**
```

dist

```

### 3. Add Environment Variables:
```

VITE_PROD_API_URL=[https://USERNAME---SPACE_NAME.hf.space](https://USERNAME---SPACE_NAME.hf.space)

```

### 4. IMPORTANT – Fix Vite Refresh Issue  
Create `_redirects` file in `public/`:

```

/*   /index.html   200

```

Allows react-router pages like:
- /search
- /register
- /admin/login

---

# 🟧 Known Deployment Notes

### HuggingFace Free CPU:
- Cannot run heavy models (SCRFD 10g)
- Use **SCRFD 2.5g ONNX** instead

### Netlify Timeout (18 min build)
- Caused by running `npm run dev`  
- Must use `npm run build`

---

# 🟣 Final Deployment Checklist

| Component | Status |
|----------|--------|
| Backend running on HF Spaces | ✔ |
| SCRFD 2.5g ONNX installed | ✔ |
| ArcFace ONNX loaded | ✔ |
| Qdrant cloud connected | ✔ |
| Redis caching working | ✔ |
| Netlify build succeeds | ✔ |
| API URL correctly set | ✔ |
| Refresh & routing fixed | ✔ |

---

# 🎉 Your app is now fully deployed!
```

