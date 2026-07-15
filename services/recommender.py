import pandas as pd
import numpy as np


class JobRecommender:

    def __init__(self, faiss_index, embeddings, jobs_df):
        self.index = faiss_index
        self.embeddings = embeddings
        self.jobs_df = jobs_df

    def recommend_similar_jobs(
        self,
        job_idx,
        top_k=6
    ):
        """
        Recommend jobs similar to selected job.
        """

        query_vector = self.embeddings[job_idx]

        distances, indices = self.index.search(
            np.array([query_vector]).astype(np.float32),
            top_k + 1
        )

        recommendations = []

        for idx in indices[0]:

            if idx == job_idx:
                continue

            job = self.jobs_df.iloc[idx]

            recommendations.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "experience": job["experience"]
            })

        return recommendations[:top_k]