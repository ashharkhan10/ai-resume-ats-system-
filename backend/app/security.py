"""
Passwords and login tokens.

hash_password / verify_password — passwords are never stored as plain text (Argon2).
create_token / read_token       — a signed JWT that says "this is user 5", valid for 7 days.
"""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import JWT_SECRET, TOKEN_DAYS

_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _hasher.verify(password, password_hash)


def create_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(days=TOKEN_DAYS)
    return jwt.encode({"sub": str(user_id), "exp": expires}, JWT_SECRET, algorithm="HS256")


def read_token(token: str) -> int | None:
    """Returns the user id, or None if the token is invalid or expired."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None
