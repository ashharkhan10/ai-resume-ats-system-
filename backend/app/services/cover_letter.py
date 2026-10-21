"""
Cover letter generator: a short, truthful letter in one of three tones.
"""

from app.schemas.resume import Lenient
from app.services import llm

TONES = {
    "professional": "formal, polite and clear",
    "friendly": "warm and conversational, but still professional",
    "confident": "bold and energetic, leading with achievements",
}

SYSTEM_PROMPT = """You write cover letters for students and fresh graduates.
Reply with JSON only: {"letter": "the full letter"}

Rules:
- 200-280 words, 3-4 short paragraphs, starting with "Dear Hiring Manager,".
- Use ONLY facts from the resume. Never invent experience, numbers or skills.
- Connect the student's real projects and skills to what the job needs.
- If the company name is unknown, write [Company Name].
- End with "Sincerely," and the student's name from the resume (or [Your Name])."""

MAX_RESUME_CHARS = 8000
MAX_JOB_CHARS = 4000


class _Reply(Lenient):
    letter: str = ""


def build_message(resume_text: str, target_title: str, job_description: str, tone: str) -> str:
    parts = [f"TONE: {TONES[tone]}", f"RESUME:\n{resume_text[:MAX_RESUME_CHARS]}"]
    if job_description.strip():
        parts.append(f"JOB DESCRIPTION:\n{job_description[:MAX_JOB_CHARS]}")
    elif target_title.strip():
        parts.append(f"TARGET ROLE: entry-level {target_title}")
    return "\n\n".join(parts)


def write_cover_letter(resume_text: str, target_title: str, job_description: str, tone: str) -> str:
    """Raises llm.AIUnavailable if the AI fails."""
    message = build_message(resume_text, target_title, job_description, tone)
    reply = llm.ask_ai_for(_Reply, SYSTEM_PROMPT, message, max_tokens=3000)
    if not reply.letter.strip():
        raise llm.AIUnavailable("Empty letter")
    return reply.letter.strip()
