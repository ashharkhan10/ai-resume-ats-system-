"""
Public share links:
  GET /share/{id} → the report, read-only, if its owner turned sharing on
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analysis
from app.schemas.analysis import AnalysisReport
from app.services.history import report_of

router = APIRouter(tags=["share"])


@router.get("/share/{analysis_id}", response_model=AnalysisReport)
def shared_report(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.get(Analysis, analysis_id)
    if analysis is None or not analysis.shared:
        raise HTTPException(404, detail="This link is not shared or no longer exists.")
    return report_of(analysis)
