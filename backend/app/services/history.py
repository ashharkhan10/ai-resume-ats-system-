"""
Saving analyses and turning saved rows back into reports.
"""

from sqlalchemy.orm import Session

from app.models import Analysis, User
from app.schemas.analysis import AnalysisReport
from app.schemas.extras import AnalysisSummary


def save_analysis(
    db: Session,
    user: User | None,
    report: AnalysisReport,
    file_name: str,
    resume_text: str,
    job_description: str,
) -> Analysis:
    row = Analysis(
        user_id=user.id if user else None,
        file_name=file_name[:255],
        target_title=report.target.title[:255],
        job_description=job_description,
        resume_text=resume_text,
        score=report.score,
        report=report.model_dump(exclude={"id", "file_name", "created_at", "shared"}),
        cover_letters={},
    )
    db.add(row)
    db.commit()
    return row


def report_of(row: Analysis) -> AnalysisReport:
    """The saved report, plus its id, file name, date and share status."""
    report = AnalysisReport.model_validate(row.report)
    report.id = row.id
    report.file_name = row.file_name
    report.created_at = row.created_at.isoformat()
    report.shared = row.shared
    return report


def summary_of(row: Analysis) -> AnalysisSummary:
    return AnalysisSummary(
        id=row.id,
        file_name=row.file_name,
        target_title=row.target_title,
        score=row.score,
        created_at=row.created_at.isoformat(),
    )
