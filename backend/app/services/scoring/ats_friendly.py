"""
ATS-friendly score: can hiring software read this resume easily?
Starts at 100 and loses points for common problems.
"""

import re

from app.schemas.resume import ResumeData

IDEAL_MIN_WORDS = 250
IDEAL_MAX_WORDS = 900  # roughly 1–2 pages

# Box-drawing and symbol characters that often come from tables, columns or icons.
ODD_CHARACTERS = re.compile(r"[│┤├┼┴┬╔╗╚╝═║■◆●★✓✔➤►▪]")

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def score_ats_friendly(text: str, resume: ResumeData) -> int:
    score = 100
    words = len(text.split())

    if words < IDEAL_MIN_WORDS:
        score -= 20  # too thin
    elif words > IDEAL_MAX_WORDS:
        score -= 15  # too long

    odd = len(ODD_CHARACTERS.findall(text))
    if odd > 20:
        score -= 20
    elif odd > 5:
        score -= 10

    if not EMAIL_PATTERN.search(text):
        score -= 15  # contact details may be in an image or header ATS can't read

    if not resume.all_bullets():
        score -= 20  # no bullet points found at all

    return max(0, score)
