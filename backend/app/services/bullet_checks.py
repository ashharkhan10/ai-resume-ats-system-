"""
Bullet quality checks recruiters notice straight away:

  - passive voice     "Was responsible for testing" → weak
  - first person      "I built…", "my team…"        → unprofessional on a resume
  - repeated verbs    "Developed… Developed… Developed…"
  - too long          more than ~2 lines (35+ words)
"""

import re
from collections import Counter
from dataclasses import dataclass, field

PASSIVE = re.compile(
    r"\b(was|were|been|being|is|are)\s+(\w+ly\s+)?\w+(ed|en)\b|\bresponsible for\b|\bduties included\b",
    re.IGNORECASE,
)
FIRST_PERSON = re.compile(r"\bI\b|\b(?i:me|my|mine|myself)\b")
TOO_LONG_WORDS = 35
REPEAT_LIMIT = 3  # the same opening verb this many times = repetitive


@dataclass
class BulletFindings:
    passive: list[str] = field(default_factory=list)
    first_person: list[str] = field(default_factory=list)
    repeated_verbs: list[str] = field(default_factory=list)  # e.g. ["Developed ×4"]
    too_long: list[str] = field(default_factory=list)


def _first_word(bullet: str) -> str:
    words = re.findall(r"[A-Za-z]+", bullet)
    return words[0].capitalize() if words else ""


def check_bullets(bullets: list[str]) -> BulletFindings:
    findings = BulletFindings()
    for bullet in bullets:
        if PASSIVE.search(bullet):
            findings.passive.append(bullet)
        if FIRST_PERSON.search(bullet):
            findings.first_person.append(bullet)
        if len(bullet.split()) > TOO_LONG_WORDS:
            findings.too_long.append(bullet)

    counts = Counter(_first_word(b) for b in bullets if _first_word(b))
    findings.repeated_verbs = [f"{verb} ×{n}" for verb, n in counts.most_common() if n >= REPEAT_LIMIT]
    return findings


def quality_penalty(findings: BulletFindings) -> int:
    """Points taken off the Content score (max 20)."""
    penalty = (
        3 * len(findings.passive)
        + (6 if findings.first_person else 0)
        + 3 * len(findings.repeated_verbs)
        + 2 * len(findings.too_long)
    )
    return min(20, penalty)
