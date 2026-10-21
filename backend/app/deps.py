"""
Shared helpers for routes ("dependencies" in FastAPI).

get_current_user  — the logged-in user, or 401
get_optional_user — the logged-in user, or None (for pages that work without login)
get_visible_analysis — an analysis the caller is allowed to see, or 404
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analysis, User
from app.security import read_token

_bearer = HTTPBearer(auto_error=False)


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None
    user_id = read_token(credentials.credentials)
    return db.get(User, user_id) if user_id else None


def get_current_user(user: User | None = Depends(get_optional_user)) -> User:
    if user is None:
        raise HTTPException(401, detail="Please log in first.")
    return user


def get_visible_analysis(
    analysis_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> Analysis:
    """
    Owners can see their analyses. Analyses made without an account
    can be opened by anyone who has the (random, unguessable) id.
    """
    analysis = db.get(Analysis, analysis_id)
    if analysis is None or (analysis.user_id is not None and (user is None or user.id != analysis.user_id)):
        raise HTTPException(404, detail="Report not found.")
    return analysis
