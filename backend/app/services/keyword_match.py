"""
Compares what the job asks for with what the resume shows.

A job keyword is "matched" if it appears anywhere in the resume text,
or is the same skill as one in the resume's skills list.
Required skills count twice as much as preferred ones.
"""

from app.schemas.analysis import KeywordMatch
from app.services.skills import mentioned_in, same_skill, unique

REQUIRED_WEIGHT = 2
PREFERRED_WEIGHT = 1


def _found(keyword: str, resume_text: str, resume_skills: list[str]) -> bool:
    if mentioned_in(keyword, resume_text):
        return True
    return any(same_skill(keyword, skill) for skill in resume_skills)


def match_keywords(
    resume_text: str,
    resume_skills: list[str],
    required: list[str],
    preferred: list[str],
) -> KeywordMatch | None:
    """Returns None if the job gave no keywords to compare against."""
    required = unique(required)
    preferred = [p for p in unique(preferred) if not any(same_skill(p, r) for r in required)]
    if not required and not preferred:
        return None

    matched, missing = [], []
    earned = possible = 0

    for keywords, weight in ((required, REQUIRED_WEIGHT), (preferred, PREFERRED_WEIGHT)):
        for keyword in keywords:
            possible += weight
            if _found(keyword, resume_text, resume_skills):
                matched.append(keyword)
                earned += weight
            else:
                missing.append(keyword)

    return KeywordMatch(matched=matched, missing=missing, match_pct=round(earned / possible * 100))
