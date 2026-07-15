import faiss
import numpy as np


class SemanticSearch:

    def __init__(self):
        self.index = None

    def build_index(self, embeddings):
        """
        Build FAISS IndexFlatL2 index.
        """

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            embeddings.astype(np.float32)
        )

        return self.index

    def save_index(
        self,
        path="models/faiss_index.bin"
    ):
        faiss.write_index(
            self.index,
            path
        )

    def load_index(
        self,
        path="models/faiss_index.bin"
    ):
        self.index = faiss.read_index(path)

    def search(
        self,
        query_embedding,
        top_k=10
    ):
        """
        Return top-k nearest neighbours.
        """

        distances, indices = self.index.search(
            query_embedding.astype(np.float32),
            top_k
        )

        return distances[0], indices[0]