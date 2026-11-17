import requests

url = "http://127.0.0.1:5000/match-resume"

pdf_path = "data/resumetest.pdf"

with open(pdf_path, "rb") as resume:
    response = requests.post(
        url,
        files={
            "resume": (
                "technical_test_resume.pdf",
                resume,
                "application/pdf"
            )
        }
    )

print("STATUS CODE:", response.status_code)

data = response.json()

if response.ok:
    print("\nEXTRACTED SKILLS:")
    print(data["resume_skills"])

    print("\nTOTAL JOBS:", data["total_jobs"])

    for job in data["recommendations"][:5]:
        print("\nJob:", job["title"])
        print("Company:", job["company"])
        print("Coverage:", job["coverage_percentage"], "%")
        print("Matched:", job["matched_skills"])
        print("Missing:", job["missing_skills"])
else:
    print("ERROR:", data)