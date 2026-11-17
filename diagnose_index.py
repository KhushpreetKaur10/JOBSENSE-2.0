
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

print("Loading dataset...")
df = pd.read_csv("data/jobs_30k.csv")

print("Loading embeddings...")
embeddings = np.load("models/embeddings.npy")

print("Loading FAISS index...")
index = faiss.read_index("models/faiss_index.bin")

print("\n========== DIMENSION CHECK ==========")
print("Dataset rows:", len(df))
print("Embedding rows:", len(embeddings))
print("FAISS indexed rows:", index.ntotal)
print("Embedding shape:", embeddings.shape)
print("FAISS dimension:", index.d)
print("FAISS metric:", index.metric_type)

if not (len(df) == len(embeddings) == index.ntotal):
    print("\nERROR: Dataset, embeddings and index sizes do not match.")
    raise SystemExit(1)

print("\n========== JOB ID 33 CHECK ==========")
job_id = 33
row = df.iloc[job_id]

print("ID:", job_id)
print("Title:", row["title"])
print("Company:", row["company"])
print("Skills:", str(row["skills"])[:200])

print("\n========== INDEX VECTOR CHECK ==========")
stored_vector = index.reconstruct(job_id)
embedding_vector = embeddings[job_id]

print(
    "Index vs embedding cosine:",
    float(np.dot(stored_vector, embedding_vector) /
          (np.linalg.norm(stored_vector) * np.linalg.norm(embedding_vector)))
)

print("\n========== FRESH EMBEDDING CHECK ==========")
model = SentenceTransformer("all-MiniLM-L6-v2")

job_text = (
    "Job Title: " + str(row["title"]) +
    " Skills: " + str(row["skills"]) +
    " Location: " + str(row["location"]) +
    " Experience: " + str(row["experience"]) +
    " Description: " + str(row["description"])
)

fresh_vector = model.encode(
    [job_text],
    convert_to_numpy=True
).astype(np.float32)

faiss.normalize_L2(fresh_vector)

print(
    "Fresh vs saved embedding cosine:",
    float(np.dot(fresh_vector[0], embedding_vector) /
          (np.linalg.norm(fresh_vector[0]) * np.linalg.norm(embedding_vector)))
)

print("\n========== SIMILAR JOBS FOR ID 33 ==========")
distances, indices = index.search(
    embedding_vector.reshape(1, -1).astype(np.float32),
    11
)

for rank, idx in enumerate(indices[0]):
    if idx < 0 or idx >= len(df):
        continue

    print(
        rank,
        "| ID:", idx,
        "| Similarity:", round(float(distances[0][rank]), 4),
        "| Title:", df.iloc[idx]["title"],
        "| Company:", df.iloc[idx]["company"]
    )
