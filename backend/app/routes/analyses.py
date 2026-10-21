"""
Saved analyses ("versions"):
  GET    /analyses                    → my versions, newest first
  GET    /analyses/{id}               → one full report
  DELETE /analyses/{id}               → delete one of mine
  POST   /analyses/{id}/share         → turn on the public share link
  POST   /analyses/{id}/interview     → interview questions (saved after the first time)
  POST   /analyses/{id}/cover-letter  → a cover letter in a chosen tone (saved per tone)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, get_visible_analysis
from app.models import Analysis, User
from app.schemas.analysis import AnalysisReport
from app.schemas.extras import AnalysisSummary, CoverLetter, CoverLetterIn, InterviewPrep, ShareOut
from app.services.cover_letter import write_cover_letter
from app.services.history import report_of, summary_of
from app.services.interview import make_interview_prep
from app.services.llm import AIUnavailable

router = APIRouter(prefix="/analyses", tags=["analyses"])

AI_BUSY = "Our AI is busy right now. Please try again in a minute."


@router.get("", response_model=list[AnalysisSummary])
def my_analyses(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(
        select(Analysis).where(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()).limit(50)
    )
    return [summary_of(row) for row in rows]


@router.get("/{analysis_id}", response_model=AnalysisReport)
def get_analysis(analysis: Analysis = Depends(get_visible_analysis)):
    return report_of(analysis)


@router.delete("/{analysis_id}", status_code=204)
def delete_analysis(
    analysis: Analysis = Depends(get_visible_analysis),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if analysis.user_id != user.id:
        raise HTTPException(404, detail="Report not found.")
    db.delete(analysis)
    db.commit()


@router.post("/{analysis_id}/share", response_model=ShareOut)
def share_analysis(analysis: Analysis = Depends(get_visible_analysis), db: Session = Depends(get_db)):
    analysis.shared = True
    db.commit()
    return ShareOut(id=analysis.id)


@router.post("/{analysis_id}/interview", response_model=InterviewPrep)
def interview_prep(
    fresh: bool = False,
    analysis: Analysis = Depends(get_visible_analysis),
    db: Session = Depends(get_db),
):
    if analysis.interview and not fresh:
        return InterviewPrep.model_validate(analysis.interview)

    try:
        prep = make_interview_prep(analysis.resume_text, analysis.target_title, analysis.job_description)
    except AIUnavailable as error:
        print(f"Interview prep failed: {error}")
        raise HTTPException(502, detail=AI_BUSY) from error

    analysis.interview = prep.model_dump()
    db.commit()
    return prep


@router.post("/{analysis_id}/cover-letter", response_model=CoverLetter)
def cover_letter(
    body: CoverLetterIn,
    analysis: Analysis = Depends(get_visible_analysis),
    db: Session = Depends(get_db),
):
    saved = analysis.cover_letters or {}
    if body.tone in saved and not body.fresh:
        return CoverLetter(tone=body.tone, text=saved[body.tone])

    try:
        text = write_cover_letter(analysis.resume_text, analysis.target_title, analysis.job_description, body.tone)
    except AIUnavailable as error:
        print(f"Cover letter failed: {error}")
        raise HTTPException(502, detail=AI_BUSY) from error

    # Assign a new dict so SQLAlchemy notices the change.
    analysis.cover_letters = {**saved, body.tone: text}
    db.commit()
    return CoverLetter(tone=body.tone, text=text)
