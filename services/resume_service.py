
import pymupdf
from services.skills import SkillMatcher


class ResumeAnalyzer:

    def __init__(self):
        self.skill_matcher = SkillMatcher()

    def extract_text(self, pdf_path):

        document = pymupdf.open(pdf_path)

        try:
            pages = []

            for page in document:
                pages.append(page.get_text("text"))

            return "\n".join(pages).strip()

        finally:
            document.close()

    def analyze_resume(self, pdf_path):

        resume_text = self.extract_text(pdf_path)

        if not resume_text:
            raise ValueError(
                "No readable text found in the PDF. "
                "Scanned PDFs require OCR."
            )

        skills = self.skill_matcher.extract_skills(resume_text)

        return {
            "skills": skills,
            "total_skills": len(skills),
            "resume_text": resume_text
        }
