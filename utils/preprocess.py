import re
import pandas as pd

INPUT_FILE = "data/jobs.xlsx"
OUTPUT_FILE = "data/jobs_30k.csv"


def clean_html(text):
    text = str(text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


print("Loading dataset...")

df = pd.read_excel(INPUT_FILE)

print("Original Rows:", len(df))

df = df.drop_duplicates()

df = df[
    df["jobDescription"].notna()
]

df = df[
    df["jobDescription"].str.len() > 100
]

df = df.sample(
    n=30000,
    random_state=42
)

df = df.reset_index(drop=True)

df = df.rename(
    columns={
        "companyName": "company",
        "jobDescription": "description",
        "tagsAndSkills": "skills"
    }
)

df["description"] = df["description"].apply(
    clean_html
)

df["title"] = df["title"].fillna("")
df["company"] = df["company"].fillna("")
df["skills"] = df["skills"].fillna("")
df["location"] = df["location"].fillna("")
df["experience"] = df["experience"].fillna("")
df["salary"] = df["salary"].fillna("Not Disclosed")

df["description"] = (
    df["description"]
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
)

keep_cols = [
    "title",
    "jobId",
    "company",
    "skills",
    "experience",
    "salary",
    "location",
    "description",
    "minimumSalary",
    "maximumSalary",
    "minimumExperience",
    "maximumExperience",
    "jobUploaded",
    "ReviewsCount",
    "AggregateRating"
]

df = df[keep_cols]

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Saved Rows:", len(df))
print("Columns Saved:")
print(df.columns.tolist())