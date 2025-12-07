

```markdown
# ReUnite AI – Missing Person Identification System  
Reunite people. Rebuild families. Powered by AI.

ReUnite AI is an AI-driven missing person identification platform that uses cutting-edge face recognition technology to match uploaded images with a centralized database of reported missing individuals. The system is designed for NGOs, police departments, and public deployment to support faster and more accurate identification.

---

## 🚀 Features

### 🔍 **AI-Powered Image Search**
- Upload an image
- Face detected using **SCRFD-ONNX**
- Facial embedding generated using **ArcFace – glintr100**
- Qdrant vector search returns top matches instantly  
- High accuracy even across lighting, angle, aging variations

### 📝 **Citizen Registration Portal**
- Register missing person details with image
- Data stored in PostgreSQL
- Automatically generates facial embedding

### 🛂 **Admin Panel (Secure)**
- Clerk authentication (Admin only)
- Approve/Reject new registrations
- Dashboard of pending, approved & rejected cases

### ⚡ **Fast & Scalable Infrastructure**
- Hugging Face Spaces → Backend (FastAPI + ONNXRuntime)
- Netlify → Frontend (React + Vite)
- NeonDB → PostgreSQL
- Qdrant Cloud → Vector search
- Upstash Redis → Caching
- Cloudinary → Image storage

---

## 📂 Project Structure

```

root/
│
├── src/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── routers/ (search, admin, register)
│   │   │   ├── services/ (db, detector, embedder, qdrant)
│   │   │   ├── cache/ (redis caches)
│   │   │   ├── schemas/
│   │   │   └── main.py
│   │   ├── models/ (SCRFD ONNX, ArcFace ONNX)
│   │   └── db_files/ (SQLAlchemy models)
│   │
│   └── frontend/
│       └── reunite-frontend/ (React + Vite)
│
├── requirements_backend.txt
├── Dockerfile
└── README.md

```

---

## 🧠 AI Models Used

### **1️⃣ SCRFD 2.5g ONNX (Face Detection)**
- Extremely lightweight & accurate
- Works on CPU (important for Hugging Face Spaces)
- Produces bounding boxes & 5-point landmarks
- Fast inference & stable under low RAM

### **2️⃣ ArcFace – glintr100 (Face Embedding Model)**
- ONNX inference for identity embedding
- Outputs a 512-dimensional vector per face
- Highly discriminative feature space
- L2 normalized for cosine similarity search

### **3️⃣ Qdrant Vector Search Engine**
- Stores all 512-dim facial embeddings
- Searches top-k nearest vectors
- Uses **COSINE distance**
- Payload stores metadata (image URL, person_id)

---

## 🔬 How the Embedding Pipeline Works

1. User uploads image  
2. Image decoded with OpenCV  
3. SCRFD detects & crops face  
4. Cropped face → ArcFace glintr100  
5. `/embedding = embedding / ||embedding||` (L2 normalization)  
6. Embedding sent to Qdrant for similarity search  
7. Top-k matches returned with metadata  
8. Results filtered by similarity threshold  

This ensures:
- High recall & precision
- Stable performance on low-power servers
- Real-time search

---

## 🗄 Database Design

### **PostgreSQL (NeonDB)**
**Table: `persons`**
```

id (UUID) PK
name, age, gender
last_seen_location, last_seen_date, last_seen_time
image_url
case_id (unique)
case_status
verified (admin approved)
qdrant_id
...

```

**Table: `registrations`**
```

id (UUID)
person_data (JSON)
person_image_url
status (pending / approved / rejected)
reviewed_by

```

**Table: `admin_users`**
```

id, username, password_hash

```

---

## 📡 API Endpoints (Backend)

### 🔍 Search
```

POST /search
multipart file → returns top matches

```

### 📝 Register
```

POST /register

```

### 🛂 Admin
```

POST /admin/verify/{id}
GET /admin/pending
GET /admin/approved
GET /admin/rejected

````

---

## 🧰 Tech Stack

### **Frontend**
- React + Vite
- TailwindCSS
- Clerk Authentication
- Axios

### **Backend**
- FastAPI
- ONNXRuntime (face models)
- SCRFD 2.5g ONNX
- ArcFace glintr100 ONNX
- SQLAlchemy ORM
- Redis (Upstash)
- Cloudinary

### **Databases**
- PostgreSQL (Neon)
- Qdrant Cloud
- Redis Cache

### **Deployment**
- Hugging Face Spaces (Docker Backend)
- Netlify (Frontend)

---

## 🛠 Installation (Local)

### Backend
```bash
cd src/backend
python3 -m venv backend_venv
source backend_venv/bin/activate
pip install -r requirements_backend.txt
uvicorn src.backend.app.main:app --reload
````

### Frontend

```bash
cd src/frontend/reunite-frontend
npm install
npm run dev
```

---

## 🛰 Deployment Links

* **Frontend (Netlify):** [https://your-netlify-deployment](https://your-netlify-deployment)
* **Backend (HuggingFace):** [https://huggingface.co/spaces/DaRkAnon1mous/ReUnite_AI](https://huggingface.co/spaces/DaRkAnon1mous/ReUnite_AI)

---

## 📄 Documentation

* **Deployment Guide** → `DEPLOYMENT.md`
* **Tech Stack Explanation** → `TECH_STACK.md`
* **Architecture Overview** → `ARCHITECTURE.md`
* **Model Details (SCRFD, ArcFace)** → `MODELS.md`

---

## 🤝 Contributing

Pull requests are welcome.
Please open an issue for major changes.

---

## 📞 Contact

For implementation queries or collaboration:
**Shrey Dikshant**

---

## ⭐ If you find this useful, star the repository!

````

---

# ✅ DEPLOYMENT.md

```markdown
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

```

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

---

# 📘 TECH_STACK.md

```markdown
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

---

# 📘 ARCHITECTURE.md

```markdown
# Architecture Overview – ReUnite AI

```

User → Frontend (React) → Backend API →
├── PostgreSQL (metadata)
├── Qdrant Cloud (vector search)
├── Redis (cache)
└── Cloudinary (image storage)

```

### Data Flow (Search)
1. Upload → Frontend sends image → Backend
2. Decode → Detect face (SCRFD)
3. Crop → Extract embedding (ArcFace)
4. Query Qdrant → Retrieve nearest matches
5. Fetch metadata from PostgreSQL
6. Return results

### Data Flow (Register)
1. User submits form
2. Image uploaded to Cloudinary
3. Metadata inserted to PostgreSQL
4. Embedding computed
5. Insert embedding + payload to Qdrant
6. Admin approval updates status

### Admin Flow
1. Clerk authenticates admin
2. Admin reviews pending registrations
3. Approve → entry added to Qdrant
4. Reject → removed from queue
```

---

# 📘 MODELS.md

```markdown
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

---

# ✅ All Files Are Ready

If you want, I can:
✔ Generate PDF documentation
✔ Generate a Postman Collection
✔ Generate a Project Report (college-style)
✔ Generate diagrams (UML, architecture)

Just tell me **“Generate full documentation PDF”** or **“Generate diagrams”**.
