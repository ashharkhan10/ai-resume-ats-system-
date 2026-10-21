"""
Content score: how strong the bullet points are.

  40% → bullets with a number (users, %, time saved…)
  35% → bullets that start with a strong action verb
  25% → bullets of a good length (8–30 words)
"""

import re

ACTION_VERBS = {
    "achieved", "analyzed", "architected", "automated", "boosted", "built", "collaborated",
    "created", "cut", "debugged", "decreased", "delivered", "deployed", "designed", "developed",
    "drove", "engineered", "enhanced", "established", "evaluated", "executed", "generated",
    "grew", "implemented", "improved", "increased", "integrated", "launched", "led", "managed",
    "mentored", "migrated", "optimized", "organized", "presented", "reduced", "refactored",
    "researched", "resolved", "saved", "scaled", "shipped", "simplified", "streamlined",
    "tested", "trained", "transformed", "won", "wrote",
}

# Bullets this good on a measure count as "full marks" for it.
QUANTIFIED_TARGET = 0.5  # half the bullets having a number is excellent
MIN_WORDS, MAX_WORDS = 8, 30

NUMBER_PATTERN = re.compile(r"\d")


def is_quantified(bullet: str) -> bool:
    return bool(NUMBER_PATTERN.search(bullet))


def starts_with_action_verb(bullet: str) -> bool:
    words = re.findall(r"[a-zA-Z]+", bullet)
    return bool(words) and words[0].lower() in ACTION_VERBS


def good_length(bullet: str) -> bool:
    return MIN_WORDS <= len(bullet.split()) <= MAX_WORDS


def score_content(bullets: list[str]) -> int:
    if not bullets:
        return 0

    total = len(bullets)
    quantified = sum(is_quantified(b) for b in bullets) / total
    action = sum(starts_with_action_verb(b) for b in bullets) / total
    length = sum(good_length(b) for b in bullets) / total

    score = 40 * min(1.0, quantified / QUANTIFIED_TARGET) + 35 * action + 25 * length
    return round(score)
