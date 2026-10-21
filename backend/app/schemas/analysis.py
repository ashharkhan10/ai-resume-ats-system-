"""
The report sent back to the browser after an analysis.
"""

from typing import Literal

from pydantic import BaseModel

from app.schemas.resume import Fit, LanguageIssue, Rewrite

Level = Literal["High", "Medium", "Low"]
TargetKind = Literal["job", "role", "none"]


class CategoryScore(BaseModel):
    id: str  # "keywords", "content", ...
    label: str  # "Keywords", "Content", ...
    score: int  # 0–100
    weight: int  # how much it counts toward the overall score (all weights add to 100)


class KeywordMatch(BaseModel):
    matched: list[str]
    missing: list[str]
    match_pct: int  # 0–100
    # Matched, but only listed (skills/summary) — not shown in a recent project or job
    listed_only: list[str] = []


class SkillProof(BaseModel):
    name: str
    proof: str | None  # where the skill is used, e.g. "Event portal", or None


class Issue(BaseModel):
    id: str
    level: Level
    title: str
    detail: str


class Target(BaseModel):
    kind: TargetKind
    title: str


class Check(BaseModel):
    """One line in a checklist: passed or not, with a short explanation."""

    id: str
    label: str
    ok: bool | None  # None = couldn't check / not needed
    detail: str = ""


class Stats(BaseModel):
    word_count: int
    bullets: int
    quantified_bullets: int


class AnalysisReport(BaseModel):
    score: int  # 0–100
    rating: str  # "Excellent", "Good", ...
    band: str = ""  # what likely happens: "Likely shortlisted", "Borderline", "Likely filtered out"
    summary: str  # one-line explanation of the score
    target: Target
    categories: list[CategoryScore]
    keywords: KeywordMatch | None  # None when there's no job or role
    fit: Fit | None = None  # how well the background fits the role (None without a target)
    skills: list[SkillProof]
    issues: list[Issue]
    rewrites: list[Rewrite]
    strengths: list[str]
    stats: Stats
    ats_checks: list[Check] = []  # can an ATS read this file properly?
    requirements: list[Check] = []  # experience, education, certifications asked for
    language_issues: list[LanguageIssue] = []  # spelling & grammar
    # Filled in after the report is saved
    id: str = ""
    file_name: str = ""
    created_at: str = ""
    shared: bool = False
