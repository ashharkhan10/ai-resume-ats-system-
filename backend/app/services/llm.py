"""
Talks to the Groq AI model.

ask_ai_json(system, user) → the AI's reply as a Python dict (valid JSON).
"""

import json

from app.config import GROQ_API_KEY, GROQ_MODEL


class AIUnavailable(Exception):
    """The AI couldn't answer (no key, network problem, bad reply…)."""


_client = None


def _get_client():
    """Creates the Groq client on first use (so tests don't need a key)."""
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise AIUnavailable("GROQ_API_KEY is missing in backend/.env")
        from groq import Groq

        _client = Groq(api_key=GROQ_API_KEY, timeout=40)
    return _client


def ask_ai_json(system: str, user: str, max_tokens: int = 6000) -> dict:
    try:
        response = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
            max_completion_tokens=max_tokens,
            reasoning_effort="low",  # fast answers
            response_format={"type": "json_object"},
        )
    except AIUnavailable:
        raise
    except Exception as error:  # network error, rate limit, bad key…
        raise AIUnavailable(str(error)) from error

    text = (response.choices[0].message.content or "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise AIUnavailable("The AI reply was not valid JSON") from error


def ask_ai_for(model, system: str, user: str, max_tokens: int = 4000):
    """
    Ask the AI and check the reply fits a Pydantic model.
    Tries twice, because AI replies are occasionally malformed.
    """
    from pydantic import ValidationError

    last_error: Exception | None = None
    for _ in range(2):
        try:
            return model.model_validate(ask_ai_json(system, user, max_tokens))
        except (AIUnavailable, ValidationError) as error:
            last_error = error
    raise AIUnavailable(str(last_error))
