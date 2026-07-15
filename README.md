# 🚀 JobSense - AI-Powered Job Search & Recommendation Engine

JobSense is an AI-powered semantic job search and recommendation system built using **Flask**, **Sentence Transformers**, and **FAISS**. Instead of relying on exact keyword matching, it understands the meaning of a user's query and retrieves the most relevant jobs using vector similarity search.

The system also provides **job-to-job recommendations**, **skill matching**, and rich job metadata such as salary, company ratings, reviews, and posting date.

---

# ✨ Features

## 🔍 Semantic Job Search

Search jobs using natural language queries such as:

- Python Developer
- Data Scientist
- Machine Learning Engineer
- React Developer
- Backend Developer
- Flask REST API Developer

The query is converted into an embedding using a transformer model and matched against job embeddings using FAISS cosine similarity search.

---

## 🤖 AI-Powered Recommendations

Each job result includes a **View Similar Jobs** button.

The recommendation engine:

- Finds semantically similar jobs
- Uses vector similarity search
- Returns the most relevant jobs based on job content
- Shows similarity scores for each recommendation

---

## 🎯 Similarity Scoring

Each search result displays:

- Semantic similarity score
- AI-generated relevance ranking

Example:

```text
Similarity Score: 0.82
```

Higher scores indicate stronger semantic relevance between the query and the job posting.

---

## 🔥 Dynamic Skill Matching

The application calculates a skill match percentage based on the user's search query.

Example:

```text
Query:
python backend developer
```

Matched against:

```text
Python, Flask, REST API
```

Output:

```text
Skill Match: 33.3%
Matched Skills: python
```

Example:

```text
Query:
data scientist
```

Job Title:

```text
Data Scientist
```

Output:

```text
Skill Match: 100%
Matched Skills: data, scientist
```

Unlike static keyword matching, JobSense dynamically analyzes the query terms and compares them against job titles, skills, and descriptions.

---

## 📊 Rich Job Metadata

Every result displays:

- Job Title
- Company Name
- Location
- Experience Required
- Salary Information
- Company Rating
- Review Count
- Job Posting Date
- Skills
- Description
- Similarity Score
- Skill Match Percentage
- Matched Skills

---

## 🧹 Data Cleaning Pipeline

The preprocessing pipeline:

- Removes duplicate jobs
- Removes missing descriptions
- Cleans HTML tags
- Removes unnecessary whitespace
- Samples 30,000 jobs
- Preserves important metadata

Example HTML cleanup:

```html
<p>Python Developer</p><br>
```

Becomes:

```text
Python Developer
```

---

# 🏗️ Project Architecture

```text
User Query
     │
     ▼
Sentence Transformer
     │
     ▼
Query Embedding
     │
     ▼
FAISS Similarity Search
     │
     ▼
Top Matching Jobs
     │
     ├── Similarity Score
     ├── Skill Match
     └── Similar Job Recommendations
```

---

# 📂 Project Structure

```text
AI-Powered Job Search & Recommendation Engine
│
├── app.py
│
├── data
│   ├── jobs.xlsx
│   └── jobs_30k.csv
│
├── models
│   ├── embeddings.npy
│   └── faiss_index.bin
│
├── services
│   ├── embedder.py
│   ├── build_index.py
│   └── skill_matcher.py
│
├── utils
│   └── preprocess.py
│
├── static
│   └── style.css
│
├── templates
│   ├── index.html
│   ├── results.html
│   └── recommendations.html
│
├── checkdb.py
│
└── README.md
```

---

# 🛠️ Tech Stack

## Backend

- Flask

## Machine Learning

- Sentence Transformers
- all-MiniLM-L6-v2

## Vector Search

- FAISS

## Data Processing

- Pandas
- NumPy

## Frontend

- HTML
- CSS
- Jinja2 Templates

---

# 📦 Dataset

Original Dataset Size:

```text
97,929 jobs
```

Processed Dataset:

```text
30,000 jobs
```

Stored Columns:

```text
title
jobId
company
skills
experience
salary
location
description
minimumSalary
maximumSalary
minimumExperience
maximumExperience
jobUploaded
ReviewsCount
AggregateRating
```

---

# ⚙️ Preprocessing

Run:

```bash
python utils/preprocess.py
```

Output:

```text
data/jobs_30k.csv
```

This step:

- Cleans HTML
- Removes duplicates
- Filters invalid jobs
- Keeps important metadata columns

---

# 🧠 Generate Embeddings

Run:

```bash
python services/embedder.py
```

This:

- Loads cleaned jobs
- Creates semantic embeddings
- Normalizes vectors
- Saves embeddings

Output:

```text
models/embeddings.npy
```

Embedding Dimension:

```text
384
```

---

# ⚡ Build FAISS Index

Run:

```bash
python services/build_index.py
```

Output:

```text
models/faiss_index.bin
```

Used for ultra-fast similarity search.

---

# 🚀 Start Application

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🔎 Example Searches

## Example 1

Query:

```text
python developer
```

Possible Results:

```text
Python Developer
Backend Engineer
Flask Developer
API Developer
```

---

## Example 2

Query:

```text
data scientist
```

Possible Results:

```text
Data Scientist
Machine Learning Engineer
AI Engineer
Data Science Consultant
```

---

## Example 3

Query:

```text
react developer
```

Possible Results:

```text
React Developer
Frontend Engineer
React Native Developer
JavaScript Developer
```

---

# 📈 Recommendation Engine

For every job result:

```text
View Similar Jobs
```

The system:

1. Takes the selected job embedding
2. Searches the FAISS index
3. Retrieves nearest job vectors
4. Displays recommended jobs

Example URL:

```text
/recommend/100
```

Meaning:

```text
Show jobs similar to job with ID 100
```

---

# 🌟 Future Enhancements

- Resume Upload
- Resume-to-Job Matching
- Skill Gap Analysis
- Salary Prediction
- Personalized Recommendations
- Job Bookmarking
- User Authentication
- Application Tracking Dashboard
- Hybrid Search (Semantic + Keyword)
- LLM-Based Job Summaries

---

# 👩‍💻 Author

**Khushpreet Kaur**


---

# 📄 License

This project is developed for educational, research, and portfolio purposes.