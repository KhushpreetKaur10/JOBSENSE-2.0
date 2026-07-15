import faiss
import numpy as np


print("Loading embeddings...")

embeddings = np.load(
    "models/embeddings.npy"
)


print("Embeddings Shape:", embeddings.shape)


dimension = embeddings.shape[1]


print("Building FAISS cosine similarity index...")


index = faiss.IndexFlatIP(
    dimension
)


index.add(
    embeddings.astype(np.float32)
)


faiss.write_index(
    index,
    "models/faiss_index.bin"
)


print(
    f"Indexed {index.ntotal} jobs successfully."
)


print("FAISS index saved.")