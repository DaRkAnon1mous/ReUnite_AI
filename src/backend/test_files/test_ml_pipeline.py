import cv2
from ..app.pipeline import extract_embedding

img = cv2.imread("data/processed/cropped_0001.jpg")
emb = extract_embedding(img)

print("Embedding length:", len(emb))
print("First 5 values:", emb[:5])
print("Norm:", sum([x*x for x in emb]) ** 0.5)# If Norm is ~1 → L2 normalization correct
