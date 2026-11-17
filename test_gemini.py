from services.llm_service import generate_response

response = generate_response(
    "Explain what Retrieval Augmented Generation (RAG) is in 3 sentences."
)

print(response)