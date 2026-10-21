"""
API tests: accounts, saving versions, sharing, interview prep and cover letters.
"""

import app.services.llm as llm
from tests.conftest import sign_up, upload


# ---------- accounts ----------

def test_register_login_and_me(client):
    headers = sign_up(client)
    assert client.get("/auth/me", headers=headers).json()["email"] == "priya@example.com"

    response = client.post("/auth/login", json={"email": "PRIYA@example.com", "password": "secret123"})
    assert response.status_code == 200
    assert response.json()["token"]


def test_login_without_account_says_create_one(client):
    response = client.post("/auth/login", json={"email": "nobody@example.com", "password": "secret123"})
    assert response.status_code == 404
    assert "create an account" in response.json()["detail"]


def test_wrong_password_and_duplicate_email(client):
    sign_up(client)
    assert client.post("/auth/login", json={"email": "priya@example.com", "password": "wrongpass"}).status_code == 401
    again = client.post("/auth/register", json={"email": "priya@example.com", "password": "secret123"})
    assert again.status_code == 409


def test_short_password_is_rejected(client):
    response = client.post("/auth/register", json={"email": "a@example.com", "password": "123"})
    assert response.status_code == 422


# ---------- versions ----------

def test_analysis_is_saved_to_my_versions(client):
    headers = sign_up(client)
    report = upload(client, headers)
    assert report["id"] and report["file_name"] == "cv.pdf"

    versions = client.get("/analyses", headers=headers).json()
    assert [v["id"] for v in versions] == [report["id"]]
    assert client.get(f"/analyses/{report['id']}", headers=headers).json()["score"] == report["score"]


def test_others_cannot_see_my_report(client):
    mine = upload(client, sign_up(client))
    stranger = sign_up(client, email="other@example.com")
    assert client.get(f"/analyses/{mine['id']}", headers=stranger).status_code == 404
    assert client.get(f"/analyses/{mine['id']}").status_code == 404


def test_analyze_needs_login(client):
    files = {"resume": ("cv.pdf", b"fake pdf", "application/pdf")}
    assert client.post("/analyze", files=files).status_code == 401


def test_delete_version(client):
    headers = sign_up(client)
    report = upload(client, headers)
    assert client.delete(f"/analyses/{report['id']}", headers=headers).status_code == 204
    assert client.get("/analyses", headers=headers).json() == []


def test_versions_need_login(client):
    assert client.get("/analyses").status_code == 401


# ---------- share links ----------

def test_share_link_only_works_after_sharing(client):
    headers = sign_up(client)
    report = upload(client, headers)
    assert client.get(f"/share/{report['id']}").status_code == 404

    client.post(f"/analyses/{report['id']}/share", headers=headers)
    shared = client.get(f"/share/{report['id']}")
    assert shared.status_code == 200
    assert shared.json()["shared"] is True


# ---------- interview prep & cover letter ----------

def test_interview_prep_is_saved_after_first_call(client, monkeypatch):
    calls = []

    def fake_ai(system, user, max_tokens=4000):
        calls.append(user)
        return {"questions": [{"type": "Project", "question": "Tell me about Event Portal.", "why": "x", "tip": "y"}]}

    monkeypatch.setattr(llm, "ask_ai_json", fake_ai)
    headers = sign_up(client)
    report = upload(client, headers)

    first = client.post(f"/analyses/{report['id']}/interview", headers=headers).json()
    second = client.post(f"/analyses/{report['id']}/interview", headers=headers).json()
    assert first == second
    assert first["questions"][0]["question"] == "Tell me about Event Portal."
    assert len(calls) == 1  # second time came from the database


def test_cover_letter_per_tone(client, monkeypatch):
    monkeypatch.setattr(llm, "ask_ai_json", lambda s, u, max_tokens=3000: {"letter": f"Dear Hiring Manager, {u[:20]}"})
    headers = sign_up(client)
    report = upload(client, headers)

    letter = client.post(f"/analyses/{report['id']}/cover-letter", json={"tone": "friendly"}, headers=headers).json()
    assert letter["tone"] == "friendly"
    assert letter["text"].startswith("Dear Hiring Manager")


def test_ai_failure_gives_friendly_error(client, monkeypatch):
    def broken(*args, **kwargs):
        raise llm.AIUnavailable("down")

    monkeypatch.setattr(llm, "ask_ai_json", broken)
    headers = sign_up(client)
    report = upload(client, headers)
    response = client.post(f"/analyses/{report['id']}/interview", headers=headers)
    assert response.status_code == 502
    assert "try again" in response.json()["detail"]
