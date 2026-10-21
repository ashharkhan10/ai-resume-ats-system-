"""
Interview prep: questions an interviewer is likely to ask, based on
this student's resume and the job/role they're applying for.
"""

from app.schemas.extras import InterviewPrep
from app.services import llm

SYSTEM_PROMPT = """You are a friendly interview coach for students and fresh graduates.
Reply with JSON only, in this shape:
{"questions": [{"type": "Technical|Project|Behavioral|HR", "question": "", "why": "", "tip": ""}]}

Rules:
- Write 8 questions: 3 Technical, 2 Project, 2 Behavioral, 1 HR.
- Base them on the real projects, skills and experience in the resume, and on the target job.
- "why": one short sentence on what the interviewer wants to learn.
- "tip": one or two sentences on how to answer well, pointing to something real in the resume.
- Simple, clear English."""

MAX_RESUME_CHARS = 8000
MAX_JOB_CHARS = 4000


def build_message(resume_text: str, target_title: str, job_description: str) -> str:
    parts = [f"RESUME:\n{resume_text[:MAX_RESUME_CHARS]}"]
    if job_description.strip():
        parts.append(f"JOB DESCRIPTION:\n{job_description[:MAX_JOB_CHARS]}")
    elif target_title.strip():
        parts.append(f"TARGET ROLE: entry-level {target_title}")
    else:
        parts.append("TARGET ROLE: the kind of job this resume is aimed at")
    return "\n\n".join(parts)


def make_interview_prep(resume_text: str, target_title: str, job_description: str) -> InterviewPrep:
    """Raises llm.AIUnavailable if the AI fails."""
    message = build_message(resume_text, target_title, job_description)
    prep = llm.ask_ai_for(InterviewPrep, SYSTEM_PROMPT, message)
    prep.questions = [q for q in prep.questions if q.question.strip()][:10]
    if not prep.questions:
        raise llm.AIUnavailable("No questions came back")
    return prep
