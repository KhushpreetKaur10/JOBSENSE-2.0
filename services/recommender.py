
import re
from datetime import datetime

from services.resume_service import ResumeAnalyzer
from services.matching_service import ResumeJobMatcher
from services.rag_service import retrieve_jobs


class ResumeRecommendationService:

    NUMBER_WORDS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "fifteen": 15,
        "twenty": 20
    }

    MONTHS = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12
    }

    def __init__(self, skill_matcher):
        self.resume_analyzer = ResumeAnalyzer()
        self.job_matcher = ResumeJobMatcher(skill_matcher)

    @classmethod
    def _number_to_float(cls, value):
        value = value.lower().strip()

        if value in cls.NUMBER_WORDS:
            return float(cls.NUMBER_WORDS[value])

        try:
            return float(value)
        except ValueError:
            return None

    @classmethod
    def _extract_explicit_experience(cls, resume_text):
        """
        Extract explicitly stated experience:
        2 years of experience
        3+ years experience
        five years' tenure
        2.5 years of professional experience
        """

        number = r"(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty)"

        patterns = [
            rf"{number}\s*\+?\s*years?\s*(?:of\s+)?(?:professional\s+)?experience",
            rf"{number}\s*\+?\s*years?[’']?\s+tenure",
            rf"experience\s*[:\-]\s*{number}\s*\+?\s*years?"
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                resume_text,
                flags=re.IGNORECASE
            )

            if match:
                value = cls._number_to_float(match.group(1))

                if value is not None:
                    return value

        return None

    @staticmethod
    def _get_employment_section(resume_text):
        """
        Extract only the employment/work experience section.
        Avoid calculating experience from education dates.
        """

        start_pattern = re.search(
            r"^\s*(?:employment history|work experience|"
            r"professional experience|employment experience)\s*$",
            resume_text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if not start_pattern:
            return ""

        remaining_text = resume_text[start_pattern.end():]

        end_pattern = re.search(
            r"^\s*(?:education|academic background|courses|"
            r"certifications|technical skills|skills|projects|"
            r"achievements|hobbies|languages|details)\s*$",
            remaining_text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if end_pattern:
            return remaining_text[:end_pattern.start()]

        return remaining_text

    @classmethod
    def _parse_month_year(cls, month_text, year_text):
        month = cls.MONTHS.get(month_text.lower().rstrip("."))

        if month is None:
            return None

        try:
            year = int(year_text)

            if year < 1900 or year > datetime.now().year + 1:
                return None

            return year * 12 + month - 1

        except ValueError:
            return None

    @classmethod
    def _extract_employment_duration(cls, resume_text):
        """
        Calculate employment duration from date ranges
        inside an employment history section.

        Overlapping date ranges are merged to avoid
        double-counting simultaneous jobs.
        """

        section = cls._get_employment_section(resume_text)

        if not section:
            return None

        date_pattern = re.compile(
            r"\b("
            + "|".join(cls.MONTHS.keys())
            + r")\.?\s+(\d{4})\s*"
            r"(?:[-–—]|to)\s*"
            r"("
            + "|".join(cls.MONTHS.keys())
            + r")\.?\s+(\d{4})\b",
            flags=re.IGNORECASE
        )

        intervals = []

        for match in date_pattern.finditer(section):
            start = cls._parse_month_year(
                match.group(1),
                match.group(2)
            )

            end = cls._parse_month_year(
                match.group(3),
                match.group(4)
            )

            if start is not None and end is not None and end >= start:
                intervals.append((start, end))

        if not intervals:
            return None

        intervals.sort()

        merged = []
        current_start, current_end = intervals[0]

        for start, end in intervals[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end

        merged.append((current_start, current_end))

        total_months = sum(
            end - start + 1
            for start, end in merged
        )

        return round(total_months / 12, 2)

    @classmethod
    def extract_candidate_experience(cls, resume_text):
        """
        Priority:
        1. Explicitly stated experience or tenure.
        2. Employment date ranges.
        3. None if reliable information is unavailable.
        """

        if not resume_text:
            return None

        explicit_experience = cls._extract_explicit_experience(
            resume_text
        )

        if explicit_experience is not None:
            return explicit_experience

        return cls._extract_employment_duration(resume_text)

    def recommend(self, resume_path, model, index, jobs_df):

        resume_data = self.resume_analyzer.analyze_resume(
            resume_path
        )

        resume_skills = resume_data["skills"]
        resume_text = resume_data["resume_text"]

        if not resume_skills:
            raise ValueError(
                "No recognized technical skills found in this resume."
            )

        candidate_experience_years = (
            self.extract_candidate_experience(resume_text)
        )

        query = (
            "Technical skills: "
            + ", ".join(resume_skills)
            + "\nResume content: "
            + resume_text[:2000]
        )

        retrieved_jobs = retrieve_jobs(
            query=query,
            model=model,
            index=index,
            jobs_df=jobs_df,
            top_k=20
        )

        recommendations = self.job_matcher.compare_jobs(
            resume_skills,
            retrieved_jobs,
            candidate_experience_years
        )

        return {
            "resume_skills": resume_skills,
            "total_skills": len(resume_skills),
            "candidate_experience_years": candidate_experience_years,
            "total_jobs": len(recommendations),
            "recommendations": recommendations
        }
