"""
Request and response shapes for sign-up and login.
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    name: str = Field("", max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str


class TokenOut(BaseModel):
    token: str
    user: UserOut
