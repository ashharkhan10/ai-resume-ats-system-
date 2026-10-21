"""
Hard requirements a job asks for, checked like an ATS "knock-out" filter:

  - years of experience ("2+ years")
  - seniority ("Senior" roles need real experience)
  - education ("B.Tech in CS or related")
  - certifications ("AWS Certified")

Each check is passed (ok=True), failed (ok=False) or not asked for (left out).
"""

from app.schemas.analysis import Check
from app.schemas.resume import AIReading
from app.services.skills import mentioned_in, same_skill

SENIOR_WORDS = ("senior", "lead", "principal", "staff", "manager")
SENIOR_MIN_MONTHS = 36


def experience_months(reading: AIReading) -> int:
    return sum(job.months for job in reading.resume.experience)


def _years(months: int) -> str:
    years = months / 12
    if months == 0:
        return "no work experience"
    if years < 1:
        return f"about {months} months"
    return f"about {years:.1f}".rstrip("0").rstrip(".") + " years"


def check_requirements(reading: AIReading, text: str) -> list[Check]:
    target, resume = reading.target, reading.resume
    months = experience_months(reading)
    checks: list[Check] = []

    if target.min_years:
        needed = round(target.min_years * 12)
        checks.append(Check(
            id="years", label=f"{target.min_years:g}+ years of experience",
            ok=months >= needed,
            detail=f"You show {_years(months)}." + ("" if months >= needed else " Internships and freelance work count — add their dates."),
        ))

    if any(word in target.seniority.lower() for word in SENIOR_WORDS) and not target.min_years:
        checks.append(Check(
            id="seniority", label=f"{target.seniority.title()}-level experience",
            ok=months >= SENIOR_MIN_MONTHS,
            detail=f"Senior roles usually expect 3+ years. You show {_years(months)}.",
        ))

    if target.education.strip():
        met = reading.fit.education_met
        degrees = ", ".join(e.degree for e in resume.education if e.degree) or "no degree listed"
        checks.append(Check(
            id="education", label=f"Education: {target.education}", ok=met,
            detail=f"Your resume shows: {degrees}.",
        ))

    for cert in target.certifications:
        has_it = mentioned_in(cert, text) or any(same_skill(cert, c) for c in resume.certifications)
        checks.append(Check(
            id=f"cert:{cert.lower()}", label=f"Certification: {cert}", ok=has_it,
            detail="Found on your resume." if has_it else "Not found. Add it if you have it, with the year.",
        ))

    return checks


def score_requirements(checks: list[Check]) -> int:
    """% of the checkable requirements that are met. 100 if the job asks for none."""
    known = [c for c in checks if c.ok is not None]
    if not known:
        return 100
    return round(sum(1 for c in known if c.ok) / len(known) * 100)
