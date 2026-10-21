"""
GET /health → {"status": "ok"}. Used to check the backend is running.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}
