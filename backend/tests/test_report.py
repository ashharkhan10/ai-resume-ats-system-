"""
Tests for the full report (scoring + issues) and the AI reader — without a real AI.
"""

import app.services.ai_reader as ai_reader
from app.services.ai_reader import ReadingFailed, build_message, read_with_ai
from app.services.analyzer import build_report
from app.schemas.resume import Fit
from app.services.llm import AIUnavailable
from tests.sample import SAMPLE_TEXT, sample_reading


def test_report_with_a_job():
    reading = sample_reading(title="Frontend Developer", required_skills=["React", "TypeScript"])
    report = build_report(SAMPLE_TEXT, reading, "job")

    assert 0 <= report.score <= 100
    assert report.target.title == "Frontend Developer"
    assert report.keywords.missing == ["TypeScript"]
    assert [c.id for c in report.categories] == [
        "keywords", "role_fit", "content", "formatting", "skill_proof", "ats_friendly"
    ]
    assert sum(c.weight for c in report.categories) == 100
    assert report.stats.bullets == 3
    assert report.stats.quantified_bullets == 2


def test_report_without_a_target_has_no_keywords():
    report = build_report(SAMPLE_TEXT, sample_reading(), "none")
    assert report.keywords is None
    assert report.fit is None
    assert "role_fit" not in [c.id for c in report.categories]


def test_wrong_field_resume_scores_low():
    """A good frontend resume checked against Product Manager must NOT score high."""
    reading = sample_reading(
        title="Product Manager",
        required_skills=["Product roadmapping", "User research", "A/B testing", "Stakeholder management", "SQL"],
    )
    reading.fit = Fit(score=15, verdict="Frontend developer with no product experience.",
                      gaps=["No product management experience"])
    report = build_report(SAMPLE_TEXT, reading, "role")

    assert report.score <= 40
    assert report.rating == "Needs work"
    assert "isn't a match for Product Manager" in report.summary
    assert report.issues[0].id == "role_mismatch"
    assert "No product management experience" in report.issues[0].detail


def test_good_fit_resume_is_not_capped():
    reading = sample_reading(title="Frontend Developer", required_skills=["React", "Node.js", "HTML", "CSS"])
    reading.fit = Fit(score=85)
    report = build_report(SAMPLE_TEXT, reading, "job")
    assert report.score >= 70
    assert "role_mismatch" not in [i.id for i in report.issues]


def test_issues_are_ordered_high_first():
    reading = sample_reading(required_skills=["TypeScript", "GraphQL", "AWS"])
    issues = build_report(SAMPLE_TEXT, reading, "job").issues
    levels = [i.level for i in issues]
    assert levels == sorted(levels, key=["High", "Medium", "Low"].index)
    assert issues[0].id == "missing_keywords"


def test_message_includes_the_job_or_the_role():
    assert "JOB DESCRIPTION" in build_message("resume", "We need React", "")
    assert "TARGET ROLE: Data Analyst" in build_message("resume", "", "Data Analyst")


def test_ai_reply_with_nulls_still_works(monkeypatch):
    reply = {"resume": {"name": "Priya", "email": None, "skills": ["SQL"]}, "target": None}
    monkeypatch.setattr(ai_reader, "ask_ai_json", lambda system, user: reply)
    reading = read_with_ai("resume text")
    assert reading.resume.email == ""
    assert reading.target.required_skills == []


def test_ai_failure_gives_a_friendly_error(monkeypatch):
    def broken(system, user):
        raise AIUnavailable("network down")

    monkeypatch.setattr(ai_reader, "ask_ai_json", broken)
    try:
        read_with_ai("resume text")
        assert False, "should have failed"
    except ReadingFailed as error:
        assert "try again" in str(error)
