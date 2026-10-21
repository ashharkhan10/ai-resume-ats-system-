"""
Formatting score: are the sections a recruiter expects actually there?
Each check adds points; the total is 100.
"""

from app.schemas.resume import ResumeData

MIN_SKILLS = 5


def score_formatting(resume: ResumeData) -> int:
    checks = [
        (15, bool(resume.email.strip())),
        (10, bool(resume.phone.strip())),
        (10, len(resume.summary.split()) >= 15),
        (20, len(resume.skills) >= MIN_SKILLS),
        (25, bool(resume.experience or resume.projects)),
        (20, bool(resume.education)),
    ]
    return sum(points for points, passed in checks if passed)
