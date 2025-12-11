
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

* **Frontend (Netlify):** https://reuniteai.netlify.app/
* **Backend (HuggingFace):** https://darkanon1mous-reunite-ai.hf.space/

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

