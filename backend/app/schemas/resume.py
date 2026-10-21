"""
The structured resume the AI reads out of the raw text.

The AI must reply in this shape. Pydantic checks it, fills in safe
defaults for anything missing, and rejects anything broken.
"""

from pydantic import BaseModel, field_validator, model_validator


class Lenient(BaseModel):
    """
    A model that treats missing or null fields as "use the default".
    AI replies often say "email": null — that shouldn't break anything.
    """

    @model_validator(mode="before")
    @classmethod
    def drop_nulls(cls, data):
        if isinstance(data, dict):
            return {key: value for key, value in data.items() if value is not None}
        return data


class Experience(Lenient):
    title: str = ""
    company: str = ""
    months: int = 0
    bullets: list[str] = []

    @field_validator("months", mode="before")
    @classmethod
    def sensible_months(cls, value) -> int:
        """Bad or silly values from the AI become 0 instead of breaking the reply."""
        try:
            months = int(value)
        except (TypeError, ValueError):
            return 0
        return months if 0 <= months <= 600 else 0


class Project(Lenient):
    title: str = ""
    technologies: list[str] = []
    bullets: list[str] = []


class Education(Lenient):
    degree: str = ""
    institution: str = ""
    year: str = ""


class ResumeData(Lenient):
    name: str = ""
    email: str = ""
    phone: str = ""
    links: list[str] = []
    summary: str = ""
    skills: list[str] = []
    experience: list[Experience] = []
    projects: list[Project] = []
    education: list[Education] = []
    certifications: list[str] = []

    def all_bullets(self) -> list[str]:
        """Every bullet point from experience and projects."""
        bullets = [b for job in self.experience for b in job.bullets]
        bullets += [b for project in self.projects for b in project.bullets]
        return [b.strip() for b in bullets if b.strip()]


class TargetData(Lenient):
    """What the job (or role) asks for."""

    title: str = ""
    required_skills: list[str] = []
    preferred_skills: list[str] = []


class Rewrite(Lenient):
    before: str
    after: str
    why: str = ""


class AIReading(Lenient):
    """Everything the single AI call returns."""

    resume: ResumeData
    target: TargetData = TargetData()
    rewrites: list[Rewrite] = []
    strengths: list[str] = []
