"""
Spelling & grammar mistakes found by the AI — checked so we never show made-up ones.

A mistake is kept only if its text really appears in the resume and the fix is different.
"""

from app.schemas.resume import LanguageIssue

MAX_ISSUES = 8


def real_language_issues(issues: list[LanguageIssue], resume_text: str) -> list[LanguageIssue]:
    text = " ".join(resume_text.lower().split())
    kept, seen = [], set()
    for issue in issues:
        wrong, fix = issue.text.strip(), issue.fix.strip()
        key = wrong.lower()
        if not wrong or not fix or key == fix.lower() or key in seen:
            continue
        if " ".join(key.split()) not in text:
            continue  # the AI invented it
        seen.add(key)
        kept.append(LanguageIssue(text=wrong, fix=fix, type=issue.type if issue.type in ("spelling", "grammar") else "spelling"))
    return kept[:MAX_ISSUES]
