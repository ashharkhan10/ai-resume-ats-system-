"""
Helpers for comparing skill names.

"ReactJS", "react.js" and "React" should all count as the same skill.
"""

import re
from difflib import SequenceMatcher

# Different spellings → one standard name.
ALIASES = {
    "reactjs": "react",
    "react.js": "react",
    "angularjs": "angular",
    "vuejs": "vue",
    "vue.js": "vue",
    "nextjs": "next.js",
    "nodejs": "node.js",
    "node": "node.js",
    "expressjs": "express",
    "express.js": "express",
    "golang": "go",
    "js": "javascript",
    "ts": "typescript",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "k8s": "kubernetes",
    "sklearn": "scikit-learn",
    "postgres": "postgresql",
    "tailwindcss": "tailwind",
    "tailwind css": "tailwind",
    "amazon web services": "aws",
    "google cloud": "gcp",
    "ci/cd": "ci cd",
    "rest api": "rest apis",
    "restful apis": "rest apis",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "powerbi": "power bi",
    "dl": "deep learning",
    "cv": "computer vision",
    "llm": "llms",
    "large language models": "llms",
    "genai": "generative ai",
    "gen ai": "generative ai",
    "oop": "object oriented programming",
    "oops": "object oriented programming",
    "dsa": "data structures and algorithms",
    "ux": "user experience",
    "ui/ux": "ui ux",
}

# Characters that are part of a skill name, so a match can't stop next to them
# ("C" is not found inside "C++" or "C#", "Java" not inside "JavaScript").
NAME_CHARS = "a-z0-9+#"

# How similar two names must be (0–1) to count as the same skill.
SIMILARITY_NEEDED = 0.88


def normalize(skill: str) -> str:
    """Lower-case, tidy spaces, and map known aliases."""
    cleaned = re.sub(r"\s+", " ", skill.strip().lower())
    return ALIASES.get(cleaned, cleaned)


def same_skill(a: str, b: str) -> bool:
    """True if two skill names mean the same thing."""
    a, b = normalize(a), normalize(b)
    if a == b:
        return True
    # Short names must match exactly: "C" ≠ "C#", "Go" ≠ "Git", "R" ≠ "Rust"
    if min(len(a), len(b)) <= 3:
        return False
    return SequenceMatcher(None, a, b).ratio() >= SIMILARITY_NEEDED


def mentioned_in(skill: str, text: str) -> bool:
    """True if the skill (or its standard name) appears in the text as a whole word."""
    lowered = text.lower()
    for name in {skill.strip().lower(), normalize(skill)}:
        pattern = rf"(?<![{NAME_CHARS}]){re.escape(name)}(?![{NAME_CHARS}])"
        if name and re.search(pattern, lowered):
            return True
    return False


def unique(skills: list[str]) -> list[str]:
    """Removes duplicates (by standard name), keeping the first spelling and the order."""
    seen: set[str] = set()
    result = []
    for skill in skills:
        key = normalize(skill)
        if key and key not in seen:
            seen.add(key)
            result.append(skill.strip())
    return result
