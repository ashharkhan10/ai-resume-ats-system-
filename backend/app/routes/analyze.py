"""
POST /analyze → upload a resume (+ job description OR target role), get the report.

Steps:
  1. pull text out of the file         (text_extraction.py)
  2. one AI call to understand it      (ai_reader.py)
  3. score it and build the report     (analyzer.py)
  4. save it to your account (login required)
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas.analysis import AnalysisReport, TargetKind
from app.services.ai_reader import ReadingFailed, read_with_ai
from app.services.analyzer import build_report
from app.services.history import report_of, save_analysis
from app.services.layout_check import inspect_layout
from app.services.text_extraction import ResumeFileError, extract_text

router = APIRouter(tags=["analyze"])


@router.post("/analyze", response_model=AnalysisReport)
def analyze(  # plain "def": FastAPI runs it in a thread, so slow AI calls don't block others
    resume: UploadFile = File(..., description="PDF or DOCX, max 5 MB"),
    job_description: str = Form(""),
    target_role: str = Form(""),
    user: User = Depends(get_current_user),  # you must be logged in
    db: Session = Depends(get_db),
):
    try:
        file_bytes = resume.file.read()
        text = extract_text(file_bytes, resume.filename or "")
    except ResumeFileError as error:
        raise HTTPException(422, detail=str(error)) from error

    try:
        reading = read_with_ai(text, job_description, target_role)
    except ReadingFailed as error:
        raise HTTPException(502, detail=str(error)) from error

    # In role mode, show the role the user picked if the AI didn't name one.
    if target_role.strip() and not reading.target.title:
        reading.target.title = target_role.strip()

    layout = inspect_layout(file_bytes, resume.filename or "")
    report = build_report(text, reading, _target_kind(job_description, target_role), layout)
    row = save_analysis(db, user, report, resume.filename or "resume", text, job_description)
    return report_of(row)


def _target_kind(job_description: str, target_role: str) -> TargetKind:
    if job_description.strip():
        return "job"
    if target_role.strip():
        return "role"
    return "none"
