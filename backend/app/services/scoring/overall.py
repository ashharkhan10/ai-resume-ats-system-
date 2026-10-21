"""
Combines the category scores into one overall score (0–100).

Two sets of weights:
  - with a job or role: being RELEVANT matters most (keywords + role fit + requirements = 60%)
  - without a target: only general resume quality is judged

Relevance cap: a well-written resume for the wrong field must still score low.
So with a target, the overall score can't go above 25 + 0.75 × relevance,
where relevance = average of keyword match and role fit.
  e.g. relevance 20 → max 40,  relevance 60 → max 70,  relevance 100 → max 100
"""

from app.schemas.analysis import CategoryScore

WEIGHTS_WITH_TARGET = {
    "keywords": 30,
    "role_fit": 20,
    "requirements": 10,
    "content": 15,
    "formatting": 10,
    "skill_proof": 5,
    "ats_friendly": 10,
}

WEIGHTS_NO_TARGET = {
    "keywords": 30,
    "content": 25,
    "formatting": 15,
    "skill_proof": 15,
    "ats_friendly": 15,
}

LABELS = {
    "keywords": "Keywords",
    "role_fit": "Role fit",
    "requirements": "Requirements",
    "content": "Content",
    "formatting": "Formatting",
    "skill_proof": "Skill proof",
    "ats_friendly": "ATS friendly",
}

CAP_BASE = 25
CAP_PER_RELEVANCE = 0.75

# (lowest score, rating, one-line summary)
RATINGS = [
    (85, "Excellent", "Your resume is strong and ready to send."),
    (70, "Good", "Solid resume — a few fixes will make it stand out."),
    (50, "Fair", "Decent base, but several things are holding it back."),
    (0, "Needs work", "Important gaps — start with the high-priority fixes below."),
]

# What would likely happen to this application (lowest score, label)
BANDS_WITH_TARGET = [(75, "Likely shortlisted"), (55, "Borderline"), (0, "Likely filtered out")]
BANDS_NO_TARGET = [(75, "Ready to apply"), (55, "Needs polish"), (0, "Needs major work")]

MISMATCH_SUMMARY = "This resume isn't a match for {title} yet — see the gaps below."


def build_categories(scores: dict[str, int], has_target: bool) -> list[CategoryScore]:
    weights = WEIGHTS_WITH_TARGET if has_target else WEIGHTS_NO_TARGET
    return [
        CategoryScore(id=key, label=LABELS[key], score=scores[key], weight=weight)
        for key, weight in weights.items()
    ]


def overall_score(categories: list[CategoryScore], relevance: int | None = None) -> int:
    total = sum(c.score * c.weight for c in categories)
    score = round(total / sum(c.weight for c in categories))
    if relevance is not None:
        score = min(score, round(CAP_BASE + CAP_PER_RELEVANCE * relevance))
    return score


def rate(score: int) -> tuple[str, str]:
    for lowest, rating, summary in RATINGS:
        if score >= lowest:
            return rating, summary
    return RATINGS[-1][1], RATINGS[-1][2]


def band(score: int, has_target: bool) -> str:
    for lowest, label in BANDS_WITH_TARGET if has_target else BANDS_NO_TARGET:
        if score >= lowest:
            return label
    return ""
