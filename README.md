# JobSense – Semantic Job Search & Resume Matching Engine

JobSense is a Flask-based job search and recommendation system that uses **Sentence Transformers, FAISS, and Gemini API** to help users discover relevant job opportunities and evaluate resume compatibility.

Instead of relying only on exact keyword matching, JobSense uses semantic embeddings to retrieve relevant job listings based on the meaning of a search query. It also supports resume-based job recommendations, skill gap analysis, and retrieval-augmented question answering.

## Features

### 1. Semantic Job Search
- Search job listings using natural language queries.
- Generate query embeddings using `all-MiniLM-L6-v2`.
- Retrieve relevant jobs using FAISS vector similarity search.
- Display job details including title, company, location, salary, experience, skills, and description.

### 2. Similar Job Recommendations
- Retrieve jobs similar to a selected listing.
- Use precomputed job embeddings and FAISS similarity search.
- Display similarity scores for recommended jobs.

### 3. Resume Analysis and Job Matching
- Upload resumes in PDF format.
- Extract resume text using PyMuPDF.
- Identify technical skills using a custom skill-matching module.
- Recommend relevant jobs based on resume content.
- Calculate skill coverage and identify missing skills.
- Evaluate experience compatibility when experience information is available.
- Rank recommendations using skill coverage, semantic similarity, and experience compatibility.

### 4. Retrieval-Augmented Job Q&A
- Ask questions about job listings using natural language.
- Retrieve relevant job records using semantic search.
- Use the Gemini API to generate answers based on retrieved job information.

### 5. Skill Matching
- Extract technical skills from queries, resumes, and job descriptions.
- Normalize supported skill aliases.
- Identify matched and missing skills.
- Calculate skill coverage percentages.

## System Architecture

### Semantic Job Search

    User Query
         |
         v
    Sentence Transformer
         |
         v
    Query Embedding
         |
         v
    FAISS Vector Search
         |
         v
    Relevant Job Listings
         |
         v
    Flask Results Page

### Resume Matching

    PDF Resume
         |
         v
    Text Extraction (PyMuPDF)
         |
         v
    Technical Skill Extraction
         |
         v
    Semantic Job Retrieval
         |
         v
    Skill & Experience Comparison
         |
         v
    Ranked Job Recommendations

### Retrieval-Augmented Q&A

    User Question
         |
         v
    Semantic Retrieval
         |
         v
    Relevant Job Records
         |
         v
    Gemini API
         |
         v
    Generated Answer

## Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Semantic Search | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| Data Processing | Pandas, NumPy |
| Resume Parsing | PyMuPDF |
| LLM Integration | Gemini API |
| Frontend | HTML, CSS, Jinja2 |
| Testing | Pytest |
| Configuration | Python-dotenv |

## Dataset

The project uses a job listings dataset containing approximately **97,929 original records**.

A processed dataset of **30,000 job listings** is used by the application.

The dataset contains fields such as:

- Job title and ID
- Company
- Skills
- Experience requirements
- Salary information
- Location
- Job description
- Company ratings and reviews
- Job posting date

## Project Structure

    AI-Powered Job Search & Recommendation Engine/
    |
    ├── app.py
    |
    ├── data/
    │   └── jobs_30k.csv
    |
    ├── models/
    │   ├── embeddings.npy
    │   └── faiss_index.bin
    |
    ├── services/
    │   ├── rag_service.py
    │   ├── llm_service.py
    │   ├── skills.py
    │   ├── matching_service.py
    │   ├── recommender.py
    │   └── resume_service.py
    |
    ├── templates/
    │   ├── index.html
    │   ├── results.html
    │   └── recommendations.html
    |
    ├── static/
    │   └── style.css
    |
    ├── requirements.txt
    ├── .env
    └── README.md

## Setup and Installation

### 1. Clone the Repository

    git clone https://github.com/KhushpreetKaur10/JobSense-AI-Job-Search-Engine.git

    cd JobSense-AI-Job-Search-Engine

### 2. Create a Virtual Environment

    python -m venv venv

Activate it on Windows:

    venv\Scripts\activate

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file in the project root:

    GEMINI_API_KEY=your_gemini_api_key

Do not commit API keys or other secrets to GitHub.

### 5. Prepare Project Files

Ensure the following files are available:

    data/jobs_30k.csv
    models/embeddings.npy
    models/faiss_index.bin

The dataset, embeddings, and FAISS index must correspond to the same job records and ordering.

### 6. Run the Application

    python app.py

Open the application at:

    http://127.0.0.1:5000

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Display the home page |
| `/search` | GET | Search for relevant jobs |
| `/recommend/<job_id>` | GET | Retrieve similar jobs |
| `/ask` | POST | Ask job-related questions |
| `/match-resume` | POST | Upload a PDF resume and retrieve matching jobs |

## Testing

Run the test suite:

    pytest -v

Additional integration tests:

    python test_resume_api.py
    python test_rag.py

## Author

**Khushpreet Kaur**

B.E. Computer Science & Engineering

GitHub: [KhushpreetKaur10](https://github.com/KhushpreetKaur10)

---

## License

This project is developed for educational, research, and portfolio purposes.
