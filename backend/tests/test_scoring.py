"""
Tests for the five score categories and the overall score.
"""

from app.schemas.analysis import CategoryScore
from app.schemas.resume import ResumeData
from app.services.scoring.ats_friendly import score_ats_friendly
from app.services.scoring.content import is_quantified, score_content, starts_with_action_verb
from app.services.scoring.formatting import score_formatting
from app.services.scoring.overall import overall_score, rate
from app.services.scoring.skill_proof import find_proof, score_skill_proof
from tests.sample import SAMPLE_TEXT, sample_reading


def test_bullet_checks():
    assert is_quantified("Cut load time by 40%")
    assert not is_quantified("Worked on the website")
    assert starts_with_action_verb("Built a REST API")
    assert not starts_with_action_verb("Responsible for testing")


def test_strong_bullets_score_full_marks():
    bullets = ["Built a React dashboard used daily by 300 students on campus"] * 4
    assert score_content(bullets) == 100


def test_weak_bullets_score_low():
    assert score_content(["Did testing", "Worked on website"]) == 0


def test_no_bullets_scores_zero():
    assert score_content([]) == 0


def test_formatting_rewards_complete_sections():
    assert score_formatting(sample_reading().resume) == 100
    assert score_formatting(ResumeData()) == 0


def test_skill_proof_finds_where_skills_are_used():
    proofs = {p.name: p.proof for p in find_proof(sample_reading().resume)}
    assert proofs["React"] == "Event Portal"
    assert proofs["Docker"] is None


def test_skill_proof_score_is_a_percentage():
    proofs = find_proof(sample_reading().resume)
    # React and Node.js have proof; JavaScript, HTML, CSS, Docker don't → 2 of 6
    assert score_skill_proof(proofs) == 33


def test_ats_friendly_penalises_missing_email():
    resume = sample_reading().resume
    assert score_ats_friendly(SAMPLE_TEXT, resume) == 100
    assert score_ats_friendly(SAMPLE_TEXT.replace("priya@example.com", ""), resume) == 85


def test_overall_score_uses_weights():
    categories = [
        CategoryScore(id="a", label="A", score=100, weight=30),
        CategoryScore(id="b", label="B", score=0, weight=70),
    ]
    assert overall_score(categories) == 30


def test_ratings():
    assert rate(90)[0] == "Excellent"
    assert rate(72)[0] == "Good"
    assert rate(55)[0] == "Fair"
    assert rate(10)[0] == "Needs work"
