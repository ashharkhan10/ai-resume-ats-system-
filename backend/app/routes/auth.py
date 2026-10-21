"""
Accounts:
  POST /auth/register → create an account, get a token
  POST /auth/login    → log in, get a token
  GET  /auth/me       → who am I?
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas.auth import LoginIn, RegisterIn, TokenOut, UserOut
from app.security import create_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


def _find_user(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def _token_for(user: User) -> TokenOut:
    return TokenOut(token=create_token(user.id), user=UserOut(id=user.id, name=user.name, email=user.email))


@router.post("/register", response_model=TokenOut, status_code=201)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if _find_user(db, body.email):
        raise HTTPException(409, detail="An account with this email already exists. Please log in.")

    user = User(email=body.email.lower(), name=body.name.strip(), password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    return _token_for(user)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = _find_user(db, body.email)
    if user is None:
        raise HTTPException(404, detail="No account found with this email. Please create an account first.")
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(401, detail="Wrong password. Please try again.")
    return _token_for(user)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, name=user.name, email=user.email)
