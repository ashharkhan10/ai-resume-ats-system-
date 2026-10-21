"""
Turns the AI's reading of a resume into the full report.

This part has no AI calls — only plain, testable Python.
The AI call happens before this, in ai_reader.py.
"""

from app.schemas.analysis import AnalysisReport, Stats, Target, TargetKind
from app.schemas.resume import AIReading
from app.services.issues import build_issues
from app.services.keyword_match import match_keywords
from app.services.scoring.ats_friendly import score_ats_friendly
from app.services.scoring.content import is_quantified, score_content
from app.services.scoring.formatting import score_formatting
from app.services.scoring.overall import build_categories, overall_score, rate
from app.services.scoring.skill_proof import find_proof, score_skill_proof

# With no job or role, the keyword score comes from how many skills are listed.
SKILLS_FOR_FULL_MARKS = 12

MAX_REWRITES = 5
MAX_STRENGTHS = 4


def build_report(text: str, reading: AIReading, target_kind: TargetKind) -> AnalysisReport:
    resume = reading.resume
    bullets = resume.all_bullets()

    keywords = None
    if target_kind != "none":
        keywords = match_keywords(
            text, resume.skills, reading.target.required_skills, reading.target.preferred_skills
        )

    proofs = find_proof(resume)

    if keywords:
        keyword_score = keywords.match_pct
    else:
        keyword_score = round(min(1.0, len(resume.skills) / SKILLS_FOR_FULL_MARKS) * 100)

    categories = build_categories({
        "keywords": keyword_score,
        "content": score_content(bullets),
        "formatting": score_formatting(resume),
        "skill_proof": score_skill_proof(proofs),
        "ats_friendly": score_ats_friendly(text, resume),
    })
    score = overall_score(categories)
    rating, summary = rate(score)

    return AnalysisReport(
        score=score,
        rating=rating,
        summary=summary,
        target=Target(kind=target_kind, title=reading.target.title),
        categories=categories,
        keywords=keywords,
        skills=proofs,
        issues=build_issues(resume, text, keywords, proofs),
        rewrites=reading.rewrites[:MAX_REWRITES],
        strengths=reading.strengths[:MAX_STRENGTHS],
        stats=Stats(
            word_count=len(text.split()),
            bullets=len(bullets),
            quantified_bullets=sum(is_quantified(b) for b in bullets),
        ),
    )
