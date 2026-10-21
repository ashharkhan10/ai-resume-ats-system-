"""
Builds the "Fix these first" list: clear problems with how to fix them,
ordered High → Medium → Low.
"""

from app.schemas.analysis import Check, Issue, KeywordMatch, SkillProof
from app.schemas.resume import Fit, LanguageIssue, ResumeData
from app.services.bullet_checks import BulletFindings
from app.services.layout_check import LayoutInfo
from app.services.sections import SectionCheck
from app.services.scoring.ats_friendly import IDEAL_MAX_WORDS, IDEAL_MIN_WORDS
from app.services.scoring.content import is_quantified, starts_with_action_verb
from app.services.scoring.formatting import MIN_SKILLS

LEVEL_ORDER = {"High": 0, "Medium": 1, "Low": 2}

# Role fit below this is a serious problem; below MEDIUM_FIT it's worth a warning.
LOW_FIT = 50
MEDIUM_FIT = 70


def _list(items: list[str], limit: int = 5) -> str:
    shown = ", ".join(items[:limit])
    return shown + (f" and {len(items) - limit} more" if len(items) > limit else "")


def build_issues(
    resume: ResumeData,
    text: str,
    keywords: KeywordMatch | None,
    proofs: list[SkillProof],
    fit: Fit | None = None,
    target_title: str = "",
    *,
    layout: LayoutInfo | None = None,
    sections: SectionCheck | None = None,
    bullets: BulletFindings | None = None,
    requirements: list[Check] | None = None,
    language: list[LanguageIssue] | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    findings = bullets
    bullets = resume.all_bullets()
    words = len(text.split())
    role = target_title or "this role"

    if fit and fit.score is not None and fit.score < MEDIUM_FIT:
        gaps = f" Biggest gaps: {'; '.join(fit.gaps[:4])}." if fit.gaps else ""
        issues.append(Issue(
            id="role_mismatch",
            level="High" if fit.score < LOW_FIT else "Medium",
            title=f"Your background is a weak fit for {role}" if fit.score < LOW_FIT
            else f"Some key experience for {role} is missing",
            detail=(fit.verdict.strip() + gaps).strip()
            or f"Add projects or experience that show you can do the work of a {role}.",
        ))

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

    issues += _requirement_issues(requirements or [])

    if keywords and keywords.listed_only:
        issues.append(Issue(
            id="listed_only", level="Medium",
            title=f"{len(keywords.listed_only)} key skills are only listed, never shown",
            detail=f"{_list(keywords.listed_only)} appear only in your skills list (or an old job). "
                   "ATS and recruiters rank skills higher when a recent project or job bullet shows you using them.",
        ))

    issues += _layout_issues(layout, sections)

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

    issues += _bullet_issues(findings)

    if language:
        examples = "; ".join(f"'{i.text}' → '{i.fix}'" for i in language[:3])
        issues.append(Issue(
            id="language", level="Medium",
            title=f"{len(language)} spelling or grammar mistake{'s' if len(language) > 1 else ''}",
            detail=f"Recruiters notice these straight away. For example: {examples}.",
        ))

    if len(resume.summary.split()) < 15:
        issues.append(Issue(id="no_summary", level="Low", title="No professional summary",
                            detail="Add 2–3 lines at the top: who you are, your main skills, and the role you want."))

    return sorted(issues, key=lambda issue: LEVEL_ORDER[issue.level])


def _requirement_issues(requirements: list[Check]) -> list[Issue]:
    issues = []
    for check in requirements:
        if check.ok is not False:
            continue
        level = "Medium" if check.id.startswith("cert:") else "High"
        issues.append(Issue(id=f"req:{check.id}", level=level,
                            title=f"Requirement not met: {check.label}", detail=check.detail))
    return issues


def _layout_issues(layout: LayoutInfo | None, sections: SectionCheck | None) -> list[Issue]:
    issues = []
    if layout:
        if layout.two_columns:
            issues.append(Issue(id="columns", level="High", title="Two-column layout",
                                detail="Many ATS read straight across the page and mix your columns together. Use a single column."))
        if layout.text_boxes:
            issues.append(Issue(id="text_boxes", level="High", title="Text inside text boxes",
                                detail="Text boxes are often skipped by ATS. Move that text into the normal page."))
        if layout.contact_in_header:
            issues.append(Issue(id="contact_header", level="High", title="Contact details are in the page header",
                                detail="Many ATS ignore headers and footers. Put your name, email and phone in the main page."))
        if layout.tables:
            issues.append(Issue(id="tables", level="Medium", title=f"{layout.tables} table(s) used for layout",
                                detail="Some ATS skip or scramble table text. Use plain lines and bullets instead."))
        if layout.images:
            issues.append(Issue(id="images", level="Low", title="Images or icons found",
                                detail="ATS can't read images. Make sure nothing important (like contact icons) is only an image."))
    if sections:
        if sections.missing:
            issues.append(Issue(id="sections", level="Medium",
                                title=f"Missing standard section: {', '.join(sections.missing)}",
                                detail="ATS finds sections by their headings. Add clear headings like 'Education', 'Skills' and 'Projects'."))
        if sections.creative:
            issues.append(Issue(id="creative_headings", level="Medium", title="Creative section headings",
                                detail=f"'{', '.join(sections.creative)}' may not be recognised. Use standard names like 'Experience' or 'Projects'."))
    return issues


def _bullet_issues(findings: BulletFindings | None) -> list[Issue]:
    if not findings:
        return []
    issues = []
    if findings.first_person:
        issues.append(Issue(id="first_person", level="Medium", title="Bullets written in first person",
                            detail=f"Drop 'I' and 'my' — e.g. \"{findings.first_person[0][:80]}\". Start with the action verb instead."))
    if findings.passive:
        issues.append(Issue(id="passive", level="Low", title=f"{len(findings.passive)} bullets use passive wording",
                            detail=f"\"{findings.passive[0][:80]}\" sounds passive. Say what YOU did: 'Built…', 'Led…'."))
    if findings.repeated_verbs:
        issues.append(Issue(id="repeated_verbs", level="Low", title="Same opening verb used again and again",
                            detail=f"{', '.join(findings.repeated_verbs)}. Vary them: Built, Designed, Automated, Improved…"))
    if findings.too_long:
        issues.append(Issue(id="long_bullets", level="Low", title=f"{len(findings.too_long)} bullets are too long",
                            detail="Keep each bullet to 1–2 lines. Recruiters skim; long bullets get skipped."))
    return issues
