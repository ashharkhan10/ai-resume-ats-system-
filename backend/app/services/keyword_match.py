"""
Compares what the job asks for with what the resume shows.

A job keyword is "matched" if it appears anywhere in the resume text,
or is the same skill as one in the resume's skills list.
Required skills count twice as much as preferred ones.

Like a real ATS, WHERE a keyword appears matters:
  - used in a recent project or job bullet → full points
  - only listed (skills section, summary, old job) → LISTED_ONLY_CREDIT of the points
"""

from app.schemas.analysis import KeywordMatch
from app.services.skills import mentioned_in, same_skill, unique

REQUIRED_WEIGHT = 2
PREFERRED_WEIGHT = 1
LISTED_ONLY_CREDIT = 0.6


def _found(keyword: str, resume_text: str, resume_skills: list[str]) -> bool:
    if mentioned_in(keyword, resume_text):
        return True
    return any(same_skill(keyword, skill) for skill in resume_skills)


def match_keywords(
    resume_text: str,
    resume_skills: list[str],
    required: list[str],
    preferred: list[str],
    used_text: str | None = None,
) -> KeywordMatch | None:
    """
    Returns None if the job gave no keywords to compare against.
    used_text = text of recent project/job bullets. If not given, every match counts fully.
    """
    required = unique(required)
    preferred = [p for p in unique(preferred) if not any(same_skill(p, r) for r in required)]
    if not required and not preferred:
        return None

    matched, missing, listed_only = [], [], []
    earned = possible = 0.0

    for keywords, weight in ((required, REQUIRED_WEIGHT), (preferred, PREFERRED_WEIGHT)):
        for keyword in keywords:
            possible += weight
            if not _found(keyword, resume_text, resume_skills):
                missing.append(keyword)
                continue
            matched.append(keyword)
            if used_text is None or mentioned_in(keyword, used_text):
                earned += weight
            else:
                listed_only.append(keyword)
                earned += weight * LISTED_ONLY_CREDIT

    return KeywordMatch(
        matched=matched, missing=missing, listed_only=listed_only,
        match_pct=round(earned / possible * 100),
    )
