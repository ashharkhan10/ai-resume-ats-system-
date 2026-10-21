"""
Builds the "Fix these first" list: clear problems with how to fix them,
ordered High → Medium → Low.
"""

from app.schemas.analysis import Issue, KeywordMatch, SkillProof
from app.schemas.resume import ResumeData
from app.services.scoring.ats_friendly import IDEAL_MAX_WORDS, IDEAL_MIN_WORDS
from app.services.scoring.content import is_quantified, starts_with_action_verb
from app.services.scoring.formatting import MIN_SKILLS

LEVEL_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def _list(items: list[str], limit: int = 5) -> str:
    shown = ", ".join(items[:limit])
    return shown + (f" and {len(items) - limit} more" if len(items) > limit else "")


def build_issues(
    resume: ResumeData,
    text: str,
    keywords: KeywordMatch | None,
    proofs: list[SkillProof],
) -> list[Issue]:
    issues: list[Issue] = []
    bullets = resume.all_bullets()
    words = len(text.split())

    if not resume.email.strip():
        issues.append(Issue(id="no_email", level="High", title="No email address found",
                            detail="Put your email at the top in plain text so recruiters (and ATS) can reach you."))

    if not resume.experience and not resume.projects:
        issues.append(Issue(id="no_work", level="High", title="No experience or projects section",
                            detail="Add 2–3 projects or internships with what you built and the result."))

    if keywords and keywords.missing:
        level = "High" if keywords.match_pct < 60 else "Medium"
        issues.append(Issue(
            id="missing_keywords", level=level,
            title=f"{len(keywords.missing)} job keywords are missing",
            detail=f"The job asks for {_list(keywords.missing)}. Add the ones you really have to a bullet or your skills.",
        ))

    if bullets:
        unquantified = [b for b in bullets if not is_quantified(b)]
        if len(unquantified) / len(bullets) > 0.7:
            issues.append(Issue(
                id="no_numbers", level="High",
                title=f"{len(unquantified)} of {len(bullets)} bullets have no measurable result",
                detail="Add numbers — users, % faster, time saved, accuracy. See the AI rewrites for examples.",
            ))

        weak_starts = [b for b in bullets if not starts_with_action_verb(b)]
        if len(weak_starts) / len(bullets) > 0.5:
            issues.append(Issue(
                id="weak_verbs", level="Medium",
                title="Many bullets don't start with an action verb",
                detail="Start each bullet with a strong verb like Built, Designed, Improved or Led.",
            ))

    unproven = [p.name for p in proofs if not p.proof]
    if unproven:
        issues.append(Issue(
            id="unproven_skills", level="Medium",
            title=f"{len(unproven)} skills have no proof",
            detail=f"{_list(unproven)} are listed but never used in a project or job. Show them in a bullet, or remove them.",
        ))

    if len(resume.skills) < MIN_SKILLS:
        issues.append(Issue(id="few_skills", level="Medium", title="Skills section is thin",
                            detail=f"List at least {MIN_SKILLS} relevant tools and technologies."))

    if words > IDEAL_MAX_WORDS:
        issues.append(Issue(id="too_long", level="Medium", title="Resume is longer than it needs to be",
                            detail="For students, one page is ideal. Cut older or less relevant points."))
    elif words < IDEAL_MIN_WORDS:
        issues.append(Issue(id="too_short", level="Medium", title="Resume looks too short",
                            detail="Add detail to your projects: what you built, how, and the result."))

    if len(resume.summary.split()) < 15:
        issues.append(Issue(id="no_summary", level="Low", title="No professional summary",
                            detail="Add 2–3 lines at the top: who you are, your main skills, and the role you want."))

    return sorted(issues, key=lambda issue: LEVEL_ORDER[issue.level])
