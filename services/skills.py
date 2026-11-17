
import re


class SkillMatcher:

    def __init__(self):

        self.skill_bank = {
            "python",
            "java",
            "c++",
            "sql",
            "mysql",
            "postgresql",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "flask",
            "django",
            "fastapi",
            "redis",
            "git",
            "github",
            "linux",
            "tensorflow",
            "pytorch",
            "pandas",
            "numpy",
            "scikit-learn",
            "machine learning",
            "deep learning",
            "nlp",
            "react",
            "reactjs",
            "react.js",
            "javascript",
            "html",
            "css",
            "rest api",
            "apis",
            "microservices",
            "mongodb",
            "oracle",
            "spring",
            "spring boot",
            "nodejs",
            "node.js",
            "typescript",
            "angular",
            "bootstrap",
            "jquery",
            "devops",
            "ci/cd",
            "jenkins",
            "spark",
            "hadoop"
        }
        self.skill_aliases = {
            "reactjs": "react",
            "react.js": "react",
            "node.js": "nodejs",
            "node js": "nodejs",
            "javascript": "javascript",
            "rest api": "rest api",
            "apis": "rest api"
        }
        # Compile patterns once instead of on every extraction.
        self.skill_patterns = {
            skill: re.compile(
                r"(?<![a-z0-9])"
                + re.escape(skill)
                + r"(?![a-z0-9])",
                re.IGNORECASE
            )
            for skill in sorted(
                self.skill_bank,
                key=len,
                reverse=True
            )
        }

    def clean_text(self, text):

        text = str(text).lower()

        text = re.sub(r"<.*?>", " ", text)

        text = re.sub(
            r"[^a-z0-9+#.\-\s/]",
            " ",
            text
        )

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract_skills(self, text):
        text = self.clean_text(text)

        found = []

        for skill, pattern in self.skill_patterns.items():
            if pattern.search(text):
                canonical_skill = self.skill_aliases.get(skill, skill)

                if canonical_skill not in found:
                    found.append(canonical_skill)

        return found

    def match_score(self, query, job_text):

        query_skills = set(
            self.extract_skills(query)
        )

        job_skills = set(
            self.extract_skills(job_text)
        )

        if not query_skills:
            return 0

        matched = query_skills.intersection(
            job_skills
        )

        score = (
            len(matched) / len(query_skills)
        ) * 100

        return round(score, 2)

    def get_matched_skills(self, query, job_text):

        query_skills = set(
            self.extract_skills(query)
        )

        job_skills = set(
            self.extract_skills(job_text)
        )

        return sorted(
            query_skills.intersection(job_skills)
        )
