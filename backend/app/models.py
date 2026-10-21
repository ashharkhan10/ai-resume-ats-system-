"""
Database tables.

ats_users     — one row per account
ats_analyses  — one row per resume check (a "version")
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# JSONB on PostgreSQL, plain JSON on SQLite
JSONData = JSON().with_variant(JSONB(), "postgresql")


def now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "ats_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), default="")
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Analysis(Base):
    __tablename__ = "ats_analyses"

    # A long random id, so links can't be guessed
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    # Empty when the user wasn't logged in
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("ats_users.id", ondelete="CASCADE"), index=True, nullable=True
    )

    file_name: Mapped[str] = mapped_column(String(255), default="")
    target_title: Mapped[str] = mapped_column(String(255), default="")
    job_description: Mapped[str] = mapped_column(Text, default="")
    resume_text: Mapped[str] = mapped_column(Text, default="")  # needed for interview prep & cover letters
    score: Mapped[int] = mapped_column(Integer, default=0)

    report: Mapped[dict] = mapped_column(JSONData)  # the full AnalysisReport
    interview: Mapped[dict | None] = mapped_column(JSONData, nullable=True)  # saved interview questions
    cover_letters: Mapped[dict] = mapped_column(JSONData, default=dict)  # {"professional": "...", ...}

    shared: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
