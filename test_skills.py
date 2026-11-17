from services.skills import SkillMatcher

matcher = SkillMatcher()

sample_resume = """
Python, JavaScript, ReactJS, React.js, React,
Node.js, REST API, APIs, Docker, MySQL.
"""

skills = matcher.extract_skills(sample_resume)

print("\nNORMALIZATION TEST")
print("==================")

for skill in skills:
    print("-", skill)

print("\nTotal unique skills:", len(skills))

assert skills.count("react") == 1
assert skills.count("nodejs") == 1
assert skills.count("rest api") == 1

print("\nAll normalization tests passed!")