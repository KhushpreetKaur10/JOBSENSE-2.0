
# Import existing JobSense components
from app import model, index, jobs_df

# Import our new RAG function
from services.rag_service import answer_job_question


if __name__ == "__main__":

    query = (
        "What skills are required for Python "
        "backend developer jobs?"
    )

    print("\nSearching relevant jobs...\n")

    result = answer_job_question(
        query,
        model,
        index,
        jobs_df
    )

    print("=" * 60)
    print("JOBSENSE AI ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\n" + "=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)

    for job in result["sources"]:

        print(f"\nJob ID: {job['id']}")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Similarity: {job['similarity_score']}")
