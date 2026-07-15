from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import faiss
import re

from sentence_transformers import SentenceTransformer
from services.skills import SkillMatcher


app = Flask(__name__)


# -----------------------------
# LOAD DATA
# -----------------------------

print("Loading jobs...")

jobs_df = pd.read_csv(
    "data/jobs_30k.csv"
)


print("Loading embeddings...")

embeddings = np.load(
    "models/embeddings.npy"
)


print("Loading FAISS index...")

index = faiss.read_index(
    "models/faiss_index.bin"
)


print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


skill_matcher = SkillMatcher()


# -----------------------------
# CLEAN HTML
# -----------------------------

def clean_html(text):

    text = str(text)

    text = re.sub(
        r"<.*?>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()



# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



# -----------------------------
# SEARCH JOBS
# -----------------------------

@app.route("/search")
def search():

    query = request.args.get(
        "query",
        ""
    )

    if not query:
        return render_template(
            "results.html",
            jobs=[],
            query=""
        )

    query_embedding = model.encode(
        [query]
    ).astype(np.float32)

    faiss.normalize_L2(
        query_embedding
    )

    distances, indices = index.search(
        query_embedding,
        10
    )

    results = []

    query_skills = set(
        query.lower().split()
    )

    for rank, idx in enumerate(indices[0]):

        row = jobs_df.iloc[idx]

        job_text = (
            str(row["title"]) + " " +
            str(row["skills"]) + " " +
            str(row["description"])
        ).lower()
        
        matched_skills = []
        
        for word in query_skills:
        
            if word in job_text:
        
                matched_skills.append(word)
        
        skill_score = round(
            len(matched_skills)
            /
            max(len(query_skills), 1)
            * 100,
            1
        )

        results.append({

            "id": int(idx),

            "title": row["title"],

            "company": row["company"],

            "location": row["location"],

            "experience": row["experience"],

            "salary": row["salary"],

            "rating": row["AggregateRating"],

            "reviews": row["ReviewsCount"],

            "posted": row["jobUploaded"],

            "skills": str(
                row["skills"]
            )[:300],

            "description": clean_html(
                row["description"]
            )[:400],

            "score": round(
                float(distances[0][rank]),
                4
            ),

            "skill_match": skill_score,

            "matched_skills": ", ".join(
                matched_skills
            ) if matched_skills else "No direct skill match"

        })

    return render_template(
        "results.html",
        jobs=results,
        query=query
    )




@app.route("/recommend/<int:job_id>")
def recommend(job_id):

    if job_id >= len(jobs_df):
        return "Invalid Job ID"

    source_row = jobs_df.iloc[job_id]

    source_skills = skill_matcher.extract_skills(
        str(source_row["skills"]) + " " +
        str(source_row["description"])
    )

    query_vector = embeddings[job_id]

    distances, indices = index.search(
        np.array([query_vector]).astype(np.float32),
        6
    )

    recommendations = []

    for rank, idx in enumerate(indices[0]):

        if idx == job_id:
            continue

        row = jobs_df.iloc[idx]

        job_skills = skill_matcher.extract_skills(
            str(row["skills"]) + " " +
            str(row["description"])
        )

        skill_score = skill_matcher.match_score(
            source_skills,
            job_skills
        )

        matched_skills = list(
            set(source_skills).intersection(
                set(job_skills)
            )
        )

        recommendations.append({

            "id": int(idx),

            "title": row["title"],

            "company": row["company"],

            "location": row["location"],

            "experience": row["experience"],

            "salary": row["salary"],

            "rating": row["AggregateRating"],

            "reviews": row["ReviewsCount"],

            "posted": row["jobUploaded"],

            "skills": str(
                row["skills"]
            )[:300],

            "description": clean_html(
                row["description"]
            )[:400],

            "score": round(
                float(distances[0][rank]),
                4
            ),

            "skill_match": skill_score,

            "matched_skills": ", ".join(
                matched_skills
            ) if matched_skills else "No common skills"

        })

    return render_template(
        "recommendations.html",
        jobs=recommendations
    )







# -----------------------------
# RUN APP
# -----------------------------


if __name__ == "__main__":

    app.run(
        debug=True
    )