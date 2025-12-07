# 📘 ARCHITECTURE.md

# Architecture Overview – ReUnite AI

```

User → Frontend (React) → Backend API →
├── PostgreSQL (metadata)
├── Qdrant Cloud (vector search)
├── Redis (cache)
└── Cloudinary (image storage)

```
<img width="3600" height="2400" alt="image" src="https://github.com/user-attachments/assets/ad227309-8637-40c5-a223-a6913aa56c98" />

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
