"""
ATS-friendly score: can hiring software read this resume easily?
Starts at 100 and loses points for common problems — in the text,
in the file's layout, and in the section headings.
"""

import re

from app.schemas.resume import ResumeData
from app.services.layout_check import LayoutInfo
from app.services.sections import SectionCheck

IDEAL_MIN_WORDS = 250
IDEAL_MAX_WORDS = 900  # roughly 1–2 pages

# Box-drawing and symbol characters that often come from tables, columns or icons.
ODD_CHARACTERS = re.compile(r"[│┤├┼┴┬╔╗╚╝═║■◆●★✓✔➤►▪]")

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def score_ats_friendly(
    text: str,
    resume: ResumeData,
    layout: LayoutInfo | None = None,
    sections: SectionCheck | None = None,
) -> int:
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

    if layout:
        if layout.two_columns:
            score -= 15  # columns get mixed together
        if layout.text_boxes:
            score -= 10  # text boxes are often skipped
        if layout.tables:
            score -= 10
        if layout.contact_in_header:
            score -= 10  # many ATS ignore headers/footers
        if layout.images:
            score -= 5  # icons/photos can't be read

    if sections:
        score -= min(24, 8 * len(sections.missing))
        if sections.creative:
            score -= 5

    return max(0, score)
