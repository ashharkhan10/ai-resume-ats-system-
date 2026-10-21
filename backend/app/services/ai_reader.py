"""
ONE AI call that does all the "understanding" work:
  - reads the resume into structured data
  - reads what the job (or role) asks for
  - rewrites the weakest bullets
  - lists real strengths

All scoring is done afterwards in plain Python (see services/scoring),
so scores are consistent and testable.
"""

from pydantic import ValidationError

from app.schemas.resume import AIReading
from app.services.llm import AIUnavailable, ask_ai_json

# Long resumes are cut to this length to keep the AI fast.
MAX_RESUME_CHARS = 12000
MAX_JOB_CHARS = 6000

SYSTEM_PROMPT = """You are an expert resume reviewer and ATS (applicant tracking system) parser.
Read the resume (and the job, if given) and reply with JSON ONLY, in exactly this shape:

{
  "resume": {
    "name": "", "email": "", "phone": "",
    "links": ["LinkedIn / GitHub / portfolio URLs"],
    "summary": "the summary/objective paragraph, copied as written, or empty",
    "skills": ["every skill listed anywhere"],
    "experience": [{"title": "", "company": "", "months": 0, "bullets": ["copied exactly"]}],
    "projects": [{"title": "", "technologies": [""], "bullets": ["copied exactly"]}],
    "education": [{"degree": "", "institution": "", "year": ""}],
    "certifications": [""]
  },
  "target": {
    "title": "job title",
    "required_skills": ["must-have skills and tools, short names like 'React', 'SQL'"],
    "preferred_skills": ["nice-to-have skills"]
  },
  "rewrites": [{"before": "a weak bullet copied exactly", "after": "the improved bullet", "why": "short reason"}],
  "strengths": ["short, specific things this resume does well"]
}

Rules:
- Copy bullets EXACTLY as written. Do not invent experience, numbers or skills.
- "months": the length of each job in months (0 if unknown).
- rewrites: pick the 3-5 weakest bullets. Make each "after" start with a strong action verb,
  stay truthful to the original, and add a measurable result using a placeholder like
  [X%] or [N users] when the original has no number.
- strengths: 2-4 items, each under 12 words.
- target: if no job or role is given, leave it empty."""


class ReadingFailed(Exception):
    """The AI couldn't read the resume. The message is shown to the user."""


def build_message(resume_text: str, job_description: str, target_role: str) -> str:
    parts = [f"RESUME:\n{resume_text[:MAX_RESUME_CHARS]}"]
    if job_description.strip():
        parts.append(f"JOB DESCRIPTION:\n{job_description[:MAX_JOB_CHARS]}")
    elif target_role.strip():
        parts.append(
            f"TARGET ROLE: {target_role}\n"
            "There is no job posting. Fill 'target' with the skills a typical "
            f"entry-level {target_role} job asks for."
        )
    return "\n\n".join(parts)


def read_with_ai(resume_text: str, job_description: str = "", target_role: str = "") -> AIReading:
    message = build_message(resume_text, job_description, target_role)

    # Try twice: AI replies are occasionally malformed.
    last_error: Exception | None = None
    for _ in range(2):
        try:
            return AIReading.model_validate(ask_ai_json(SYSTEM_PROMPT, message))
        except (AIUnavailable, ValidationError) as error:
            last_error = error

    print(f"AI reading failed: {last_error}")
    raise ReadingFailed("Our AI couldn't read this resume right now. Please try again in a minute.")
