"""
Skill proof: is each listed skill actually used in a project or job?

A skill "has proof" if it's mentioned in a project's technologies or bullets,
or in a job's bullets. Score = % of skills with proof.
"""

from app.schemas.analysis import SkillProof
from app.schemas.resume import ResumeData
from app.services.skills import mentioned_in, same_skill, unique


def find_proof(resume: ResumeData) -> list[SkillProof]:
    results = []
    for skill in unique(resume.skills):
        results.append(SkillProof(name=skill, proof=_where_used(skill, resume)))
    return results


def score_skill_proof(proofs: list[SkillProof]) -> int:
    if not proofs:
        return 0
    with_proof = sum(1 for p in proofs if p.proof)
    return round(with_proof / len(proofs) * 100)


def _where_used(skill: str, resume: ResumeData) -> str | None:
    for project in resume.projects:
        in_tech = any(same_skill(skill, tech) for tech in project.technologies)
        in_bullets = mentioned_in(skill, " ".join(project.bullets))
        if in_tech or in_bullets:
            return project.title or "A project"

    for job in resume.experience:
        if mentioned_in(skill, " ".join(job.bullets)):
            return job.company or job.title or "Work experience"

    return None
