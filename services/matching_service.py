
import re


class ResumeJobMatcher:

    def __init__(self, skill_matcher):
        self.skill_matcher = skill_matcher

    @staticmethod
    def parse_experience(value):
        """Parse experience ranges such as 0-2 Yrs or 3+ years."""

        if value is None:
            return None

        text = str(value).lower().strip()

        if not text or text in {"nan", "none", "not specified"}:
            return None

        match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)",
            text
        )

        if match:
            return (
                float(match.group(1)),
                float(match.group(2))
            )

        match = re.search(r"(\d+(?:\.\d+)?)\s*\+", text)

        if match:
            return float(match.group(1)), None

        return None

    @staticmethod
    def calculate_experience_score(candidate_years, minimum):
        """Calculate compatibility with the minimum requirement."""

        if candidate_years is None or minimum is None:
            return None

        if candidate_years < minimum:
            gap = minimum - candidate_years
            return round(max(0, 100 - gap * 25), 2)

        return 100.0

    @staticmethod
    def get_experience_status(candidate_years, minimum):
        """Determine experience eligibility separately from ranking."""

        if minimum is None:
            return "Not specified"

        if candidate_years is None:
            return "Unknown"

        if candidate_years < minimum:
            return "Below requirement"

        return "Meets minimum"

    @staticmethod
    def _as_text(value):
        if value is None:
            return ""

        if isinstance(value, list):
            return ", ".join(str(item) for item in value if item)

        try:
            if value != value:
                return ""
        except Exception:
            pass

        return str(value)

    @staticmethod
    def _as_number(value):
        try:
            number = float(value)

            if number != number:
                return None

            return number

        except (TypeError, ValueError):
            return None

    def compare_job(
        self,
        resume_skills,
        job,
        candidate_experience_years=None
    ):

        resume_skill_set = {
            str(skill).strip().lower()
            for skill in resume_skills
            if str(skill).strip()
        }

        job_skills_text = self._as_text(
            job.get("skills", "")
        )

        required_skills = set(
            self.skill_matcher.extract_skills(job_skills_text)
        )

        matched_skills = sorted(
            resume_skill_set & required_skills
        )

        missing_skills = sorted(
            required_skills - resume_skill_set
        )

        coverage = None

        if required_skills:
            coverage = round(
                len(matched_skills) / len(required_skills) * 100,
                2
            )

        try:
            similarity = float(
                job.get("similarity_score", 0.0) or 0.0
            )
        except (TypeError, ValueError):
            similarity = 0.0

        semantic_score = max(
            0.0,
            min(1.0, similarity)
        ) * 100

        experience = job.get(
            "experience",
            "Not specified"
        )

        minimum = self._as_number(
            job.get("minimum_experience")
        )

        maximum = self._as_number(
            job.get("maximum_experience")
        )

        # Fall back to parsing the text if structured data is absent.
        parsed_range = self.parse_experience(experience)

        if minimum is None and parsed_range is not None:
            minimum = parsed_range[0]

        if maximum is None and parsed_range is not None:
            maximum = parsed_range[1]

        experience_score = self.calculate_experience_score(
            candidate_experience_years,
            minimum
        )

        experience_status = self.get_experience_status(
            candidate_experience_years,
            minimum
        )

        # Normalize weights across available metrics.
        components = []

        if coverage is not None:
            components.append((coverage, 0.60))

        components.append((semantic_score, 0.25))

        if experience_score is not None:
            components.append((experience_score, 0.15))

        total_weight = sum(
            weight for _, weight in components
        )

        ranking_score = sum(
            score * weight for score, weight in components
        ) / total_weight

        return {
            "id": job.get("id", job.get("jobId")),
            "title": job.get("title", "Unknown title"),
            "company": job.get("company", "Unknown company"),
            "location": job.get("location", "Not specified"),
            "skills": job_skills_text,
            "required_skills": sorted(required_skills),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_required_skills": len(required_skills),
            "skill_data_available": bool(required_skills),
            "coverage_percentage": coverage,
            "similarity_score": round(similarity, 4),
            "experience": experience,
            "minimum_experience": minimum,
            "maximum_experience": maximum,
            "candidate_experience_years": candidate_experience_years,
            "experience_score": experience_score,
            "experience_status": experience_status,
            "salary": job.get("salary", "Not specified"),
            "description": job.get("description", ""),
            "ranking_score": round(ranking_score, 2)
        }

    def compare_jobs(
        self,
        resume_skills,
        jobs,
        candidate_experience_years=None
    ):

        results = [
            self.compare_job(
                resume_skills,
                job,
                candidate_experience_years
            )
            for job in jobs
        ]

        return sorted(
            results,
            key=lambda item: (
                item["ranking_score"],
                item["similarity_score"]
            ),
            reverse=True
        )
