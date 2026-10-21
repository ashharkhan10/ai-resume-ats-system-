"""
Turns the AI's reading of a resume into the full report.

This part has no AI calls — only plain, testable Python.
The AI call happens before this, in ai_reader.py.

With a job or role, the report is judged on RELEVANCE first:
keyword match + role fit decide most of the score, and cap it
(see scoring/overall.py). Without a target, only general quality counts.
"""

from app.schemas.analysis import AnalysisReport, Stats, Target, TargetKind
from app.schemas.resume import AIReading
from app.services.issues import build_issues
from app.services.keyword_match import match_keywords
from app.services.scoring.ats_friendly import score_ats_friendly
from app.services.scoring.content import is_quantified, score_content
from app.services.scoring.formatting import score_formatting
from app.services.scoring.overall import MISMATCH_SUMMARY, build_categories, overall_score, rate
from app.services.scoring.skill_proof import find_proof, score_skill_proof

# With no job or role, the keyword score comes from how many skills are listed.
SKILLS_FOR_FULL_MARKS = 12

# Below this relevance the summary says plainly that it's not a match.
MISMATCH_BELOW = 45

MAX_REWRITES = 5
MAX_STRENGTHS = 4


def build_report(text: str, reading: AIReading, target_kind: TargetKind) -> AnalysisReport:
    resume = reading.resume
    bullets = resume.all_bullets()
    has_target = target_kind != "none"

    keywords = None
    if has_target:
        keywords = match_keywords(
            text, resume.skills, reading.target.required_skills, reading.target.preferred_skills
        )
    has_target = has_target and keywords is not None

    proofs = find_proof(resume)

    scores = {
        "content": score_content(bullets),
        "formatting": score_formatting(resume),
        "skill_proof": score_skill_proof(proofs),
        "ats_friendly": score_ats_friendly(text, resume),
    }

    fit = None
    relevance = None
    if has_target:
        fit = reading.fit
        # If the AI gave no fit score, fall back to the keyword match.
        fit_score = fit.score if fit.score is not None else keywords.match_pct
        scores["keywords"] = keywords.match_pct
        scores["role_fit"] = fit_score
        relevance = round((keywords.match_pct + fit_score) / 2)
    else:
        scores["keywords"] = round(min(1.0, len(resume.skills) / SKILLS_FOR_FULL_MARKS) * 100)

    categories = build_categories(scores, has_target)
    score = overall_score(categories, relevance)
    rating, summary = rate(score)
    if relevance is not None and relevance < MISMATCH_BELOW:
        summary = MISMATCH_SUMMARY.format(title=reading.target.title or "this role")

    return AnalysisReport(
        score=score,
        rating=rating,
        summary=summary,
        target=Target(kind=target_kind, title=reading.target.title),
        categories=categories,
        keywords=keywords,
        fit=fit,
        skills=proofs,
        issues=build_issues(resume, text, keywords, proofs, fit, reading.target.title),
        rewrites=reading.rewrites[:MAX_REWRITES],
        strengths=reading.strengths[:MAX_STRENGTHS],
        stats=Stats(
            word_count=len(text.split()),
            bullets=len(bullets),
            quantified_bullets=sum(is_quantified(b) for b in bullets),
        ),
    )
