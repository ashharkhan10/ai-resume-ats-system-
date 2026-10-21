"""
Combines the five category scores into one overall score (0–100).
"""

from app.schemas.analysis import CategoryScore

# How much each category counts. They add up to 100.
WEIGHTS = {
    "keywords": 30,
    "content": 25,
    "formatting": 15,
    "skill_proof": 15,
    "ats_friendly": 15,
}

LABELS = {
    "keywords": "Keywords",
    "content": "Content",
    "formatting": "Formatting",
    "skill_proof": "Skill proof",
    "ats_friendly": "ATS friendly",
}

# (lowest score, rating, one-line summary)
RATINGS = [
    (85, "Excellent", "Your resume is strong and ready to send."),
    (70, "Good", "Solid resume — a few fixes will make it stand out."),
    (50, "Fair", "Decent base, but several things are holding it back."),
    (0, "Needs work", "Important gaps — start with the high-priority fixes below."),
]


def build_categories(scores: dict[str, int]) -> list[CategoryScore]:
    return [
        CategoryScore(id=key, label=LABELS[key], score=scores[key], weight=weight)
        for key, weight in WEIGHTS.items()
    ]


def overall_score(categories: list[CategoryScore]) -> int:
    total = sum(c.score * c.weight for c in categories)
    return round(total / sum(c.weight for c in categories))


def rate(score: int) -> tuple[str, str]:
    for lowest, rating, summary in RATINGS:
        if score >= lowest:
            return rating, summary
    return RATINGS[-1][1], RATINGS[-1][2]
