"""
The report sent back to the browser after an analysis.
"""

from typing import Literal

from pydantic import BaseModel

from app.schemas.resume import Rewrite

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


class Stats(BaseModel):
    word_count: int
    bullets: int
    quantified_bullets: int


class AnalysisReport(BaseModel):
    score: int  # 0–100
    rating: str  # "Excellent", "Good", ...
    summary: str  # one-line explanation of the score
    target: Target
    categories: list[CategoryScore]
    keywords: KeywordMatch | None  # None when there's no job or role
    skills: list[SkillProof]
    issues: list[Issue]
    rewrites: list[Rewrite]
    strengths: list[str]
    stats: Stats
    # Filled in after the report is saved
    id: str = ""
    file_name: str = ""
    created_at: str = ""
    shared: bool = False
