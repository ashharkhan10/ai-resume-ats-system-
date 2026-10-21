"""
Shapes for saved versions, interview prep and cover letters.
"""

from typing import Literal

from pydantic import BaseModel

from app.schemas.resume import Lenient

Tone = Literal["professional", "friendly", "confident"]


class AnalysisSummary(BaseModel):
    """One row in the "My versions" list."""

    id: str
    file_name: str
    target_title: str
    score: int
    created_at: str


class InterviewQuestion(Lenient):
    type: str = "Technical"  # Technical / Project / Behavioral / HR
    question: str = ""
    why: str = ""  # why they'd ask it
    tip: str = ""  # how to answer it well


class InterviewPrep(Lenient):
    questions: list[InterviewQuestion] = []


class CoverLetterIn(BaseModel):
    tone: Tone = "professional"
    fresh: bool = False  # True = write a new one instead of the saved one


class CoverLetter(BaseModel):
    tone: Tone
    text: str


class ShareOut(BaseModel):
    id: str
