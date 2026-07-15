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

    def clean_text(self, text):

        text = str(text).lower()

        text = re.sub(r"<.*?>", " ", text)

        text = re.sub(r"[^a-z0-9+#.\-\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract_skills(self, text):

        text = self.clean_text(text)

        found = []

        for skill in self.skill_bank:

            if skill.lower() in text:
                found.append(skill.lower())

        return list(set(found))

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
            len(matched)
            /
            len(query_skills)
        ) * 100

        return round(score, 2)

    def get_matched_skills(
        self,
        query,
        job_text
    ):

        query_skills = set(
            self.extract_skills(query)
        )

        job_skills = set(
            self.extract_skills(job_text)
        )

        return list(
            query_skills.intersection(
                job_skills
            )
        )