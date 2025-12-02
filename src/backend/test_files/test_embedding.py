from src.backend.pipelines.compute_embeddings import compute_embedding

emb = compute_embedding("data/processed/cropped_0001.jpg")
print("Embedding size:", len(emb))
