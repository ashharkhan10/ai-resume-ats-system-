"""
Tests for skill name matching and job keyword matching.
"""

from app.services.keyword_match import match_keywords
from app.services.skills import mentioned_in, normalize, same_skill, unique


def test_aliases_become_one_name():
    assert normalize("ReactJS") == "react"
    assert normalize(" Node ") == "node.js"


def test_same_skill_handles_spelling_differences():
    assert same_skill("React.js", "react")
    assert same_skill("PostgreSQL", "Postgres")
    assert not same_skill("Java", "JavaScript")


def test_mentioned_in_needs_a_whole_word():
    assert mentioned_in("Go", "Built a service in Go and Python")
    assert not mentioned_in("Go", "Good teamwork")


def test_unique_removes_repeats():
    assert unique(["React", "react.js", "CSS"]) == ["React", "CSS"]


def test_keywords_found_in_text_or_skills_count_as_matched():
    result = match_keywords(
        resume_text="Built APIs with FastAPI",
        resume_skills=["ReactJS"],
        required=["React", "FastAPI", "Kubernetes"],
        preferred=[],
    )
    assert result.matched == ["React", "FastAPI"]
    assert result.missing == ["Kubernetes"]
    assert result.match_pct == 67


def test_required_skills_count_double():
    result = match_keywords("I know SQL", [], required=["SQL"], preferred=["Tableau"])
    # earned 2 (SQL) out of 3 possible (2 + 1)
    assert result.match_pct == 67


def test_no_keywords_means_no_match_result():
    assert match_keywords("anything", [], [], []) is None
