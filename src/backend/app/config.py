from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin-token")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.6"))  # 0..1
TOP_K = int(os.getenv("TOP_K", "5"))

# Model paths (relative to project root)
BUFFALO_ONNX  = os.getenv("ARCFACE_ONNX", "src/backend/models/glintr100.onnx")
SCRFD_ONNX = os.getenv("SCRFD_ONNX", "src/backend/models/SCRFD.onnx")  # optional
