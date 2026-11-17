from flask import Flask, render_template, request, jsonify
from services.rag_service import answer_job_question
import pandas as pd
import numpy as np
import faiss
import re

import os
import tempfile

from flask import jsonify, request
from services.recommender import ResumeRecommendationService

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
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

resume_recommender = ResumeRecommendationService(skill_matcher)

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

    query_skills = set(query.lower().split())

    for rank, idx in enumerate(indices[0]):

        if idx < 0 or idx >= len(jobs_df):
            continue

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
            len(matched_skills) / max(len(query_skills), 1) * 100,
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
            "skills": str(row["skills"])[:300],
            "description": clean_html(row["description"])[:400],
            "score": round(float(distances[0][rank]), 4),
            "skill_match": skill_score,
            "matched_skills": ", ".join(matched_skills)
                if matched_skills else "No direct skill match"
        })


    return render_template(
        "results.html",
        jobs=results,
        query=query
    )




@app.route("/recommend/<int:job_id>")
def recommend(job_id):

    if job_id < 0 or job_id >= len(jobs_df):
        return "Invalid Job ID", 404

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
        if idx < 0 or idx >= len(jobs_df):
            continue
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
        jobs=recommendations,
        source_job=source_row
    )




@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request must contain JSON data."
        }), 400

    query = data.get("query")

    if not isinstance(query, str) or not query.strip():
        return jsonify({
            "error": "Please enter a valid question."
        }), 400

    query = query.strip()

    if len(query) > 500:
        return jsonify({
            "error": "Question must not exceed 500 characters."
        }), 400

    try:
        result = answer_job_question(
            query,
            model,
            index,
            jobs_df
        )

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Error in /ask")

        return jsonify({
            "error": "Unable to process your question right now."
        }), 500




@app.route("/match-resume", methods=["POST"])
def match_resume():

    if "resume" not in request.files:
        return jsonify({
            "error": "No resume file was received."
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "error": "Please select a PDF file."
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are supported."
        }), 400

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:

            temp_path = temp_file.name
            file.save(temp_path)

        # Validate the actual PDF signature
        with open(temp_path, "rb") as uploaded:
            signature = uploaded.read(5)

        if signature != b"%PDF-":
            return jsonify({
                "error": "The uploaded file is not a valid PDF."
            }), 400

        app.logger.info("Starting resume analysis")

        result = resume_recommender.recommend(
            resume_path=temp_path,
            model=model,
            index=index,
            jobs_df=jobs_df,
            # top_k=20
        )

        app.logger.info(
            "Resume analysis completed. Skills: %s, Jobs: %s",
            result["total_skills"],
            result["total_jobs"]
        )

        return jsonify(result), 200

    except ValueError as error:
        app.logger.warning("Resume validation: %s", str(error))

        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        # Full traceback appears in the Flask terminal
        app.logger.exception("Unexpected error in /match-resume")

        return jsonify({
            "error": "Resume matching failed. Check the Flask terminal for the error details."
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "File too large. Maximum allowed size is 5 MB."
    }), 413

# -----------------------------
# RUN APP
# -----------------------------


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
