
import pytest

from services.skills import SkillMatcher
from services.matching_service import ResumeJobMatcher
from services.recommender import ResumeRecommendationService


@pytest.fixture
def matcher():
    return ResumeJobMatcher(SkillMatcher())


def test_experience_scoring(matcher):

    assert matcher.calculate_experience_score(0, 5) == 0
    assert matcher.calculate_experience_score(2, 5) == 25
    assert matcher.calculate_experience_score(5, 5) == 100
    assert matcher.calculate_experience_score(8, 5) == 100
    assert matcher.calculate_experience_score(None, 5) is None


def test_experience_status(matcher):

    assert matcher.get_experience_status(
        None, 5
    ) == "Unknown"

    assert matcher.get_experience_status(
        2, 5
    ) == "Below requirement"

    assert matcher.get_experience_status(
        5, 5
    ) == "Meets minimum"

    assert matcher.get_experience_status(
        None, None
    ) == "Not specified"


def test_experience_parser(matcher):

    assert matcher.parse_experience("0-2 Yrs") == (0.0, 2.0)
    assert matcher.parse_experience("5-7 Yrs") == (5.0, 7.0)
    assert matcher.parse_experience("3+ years") == (3.0, None)
    assert matcher.parse_experience("Not specified") is None


def test_skill_matching():

    skills = SkillMatcher()

    result = skills.extract_skills(
        "Python, JavaScript, GitHub, Flask and MySQL"
    )

    assert "python" in result
    assert "javascript" in result
    assert "github" in result
    assert "flask" in result
    assert "mysql" in result

    # Ensure substring false positives are avoided.
    assert "java" not in result
    assert "git" not in result


def test_recommendation_ranking(matcher):

    resume_skills = [
        "python",
        "flask",
        "mysql"
    ]

    jobs = [
        {
            "id": 1,
            "title": "Python Backend Developer",
            "company": "Company A",
            "location": "Remote",
            "skills": "Python, Flask, MySQL",
            "experience": "0-2 Yrs",
            "similarity_score": 0.8
        },
        {
            "id": 2,
            "title": "Java Developer",
            "company": "Company B",
            "location": "Delhi",
            "skills": "Java, Spring Boot",
            "experience": "5-7 Yrs",
            "similarity_score": 0.7
        }
    ]

    results = matcher.compare_jobs(
        resume_skills,
        jobs,
        candidate_experience_years=1
    )

    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[0]["coverage_percentage"] == 100
    assert results[0]["ranking_score"] > results[1]["ranking_score"]


def test_unknown_candidate_experience(matcher):

    job = {
        "id": 1,
        "title": "Python Developer",
        "skills": "Python, Flask",
        "experience": "5-10 Yrs",
        "minimum_experience": 5,
        "maximum_experience": 10,
        "similarity_score": 0.8
    }

    result = matcher.compare_job(
        ["python", "flask"],
        job,
        candidate_experience_years=None
    )

    assert result["experience_status"] == "Unknown"
    assert result["experience_score"] is None
    assert result["coverage_percentage"] == 100
