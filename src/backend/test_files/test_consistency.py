# test_consistency.py - FULL VERSION
import cv2
import numpy as np
import requests
from src.backend.app.pipeline import extract_embedding
from src.backend.app.services.qdrant_service import search_vectors

# Download test image
test_image_url = "https://res.cloudinary.com/dn9fmgufm/image/upload/v1764487688/jntvkjkkhtr0rub9dpmf.jpg"
expected_person_id = "3f91988b-cff8-48ee-a237-1e5269736388"

resp = requests.get(test_image_url)
arr = np.frombuffer(resp.content, np.uint8)
img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

print(f"📷 Image loaded: shape={img.shape}")

# Generate embedding
emb = extract_embedding(img)

if emb is None:
    print("❌ Failed to generate embedding")
    exit(1)

print(f"✅ Embedding generated: length={len(emb)}")
print(f"   First 5 values: {emb[:5]}")

# Search Qdrant
print("\n" + "="*60)
print("🔍 Searching Qdrant for matches...")
print("="*60)

results = search_vectors(emb, top_k=5)

print(f"\n📊 Found {len(results)} results:\n")

for i, hit in enumerate(results):
    person_id = hit.payload.get('person_id')
    score = hit.score
    image_url = hit.payload.get('image_url')
    
    is_match = person_id == expected_person_id
    emoji = "✅" if is_match else "❌"
    
    print(f"{emoji} Result {i+1}:")
    print(f"   Person ID: {person_id}")
    print(f"   Score: {score:.4f}")
    print(f"   Image URL: {image_url}")
    
    if is_match:
        print(f"   🎯 THIS IS THE CORRECT MATCH!")
    print()

# Analysis
top_match = results[0]
top_score = top_match.score
top_person_id = top_match.payload.get('person_id')

print("="*60)
print("📈 ANALYSIS:")
print("="*60)

if top_person_id == expected_person_id:
    if top_score >= 0.6:
        print(f"✅ PERFECT! Same image matched itself with score {top_score:.4f}")
        print("   Your embeddings are consistent!")
    else:
        print(f"⚠️  CORRECT person but LOW score ({top_score:.4f})")
        print("   Expected >0.6 for same image")
        print("   Possible issues:")
        print("   - Different preprocessing when building DB")
        print("   - Need to rebuild Qdrant with current pipeline")
else:
    print(f"❌ WRONG MATCH!")
    print(f"   Expected: {expected_person_id}")
    print(f"   Got: {top_person_id}")
    print(f"   Score: {top_score:.4f}")
    print()
    print("   ROOT CAUSE:")
    print("   - Qdrant DB was built with DIFFERENT preprocessing")
    print("   - SOLUTION: Rebuild Qdrant with current pipeline")