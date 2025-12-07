FROM python:3.12-slim

# Install OS dependencies for OpenCV + ONNXRuntime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements
COPY requirements_backend.txt ./requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# Disable GPU provider warnings in ONNXRuntime
ENV ORT_DISABLE_MEMORY_ARENA=1
ENV ORT_DISABLE_SPARSE_TENSORS=1

# Start FastAPI backend
CMD ["uvicorn", "src.backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
