import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

print("Loading jobs...")

df = pd.read_csv("data/jobs_30k.csv")

texts = (
    "Job Title: "
    + df["title"].fillna("")
    + " Skills: "
    + df["skills"].fillna("")
    + " Location: "
    + df["location"].fillna("")
    + " Experience: "
    + df["experience"].fillna("")
    + " Description: "
    + df["description"].fillna("")
)

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = model.encode(
    texts.tolist(),
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True
)

embeddings = embeddings.astype(np.float32)

faiss.normalize_L2(embeddings)

print("Embedding Shape:", embeddings.shape)

np.save(
    "models/embeddings.npy",
    embeddings
)

print("Embeddings saved successfully.")