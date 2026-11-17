from services.resume_service import ResumeAnalyzer

analyzer = ResumeAnalyzer()
pdf_path = "data/sample_resume.pdf"

result = analyzer.analyze_resume(pdf_path)

print("\nRESUME ANALYSIS")
print("======================")
print("Extracted skills:", result["total_skills"])

print("\nExtracted text length:", len(result["resume_text"]))
print("\nFirst 1000 characters of extracted text:")
print(result["resume_text"][:1000])

print("\nDetected skills:")
for skill in result["skills"]:
    print("-", skill)