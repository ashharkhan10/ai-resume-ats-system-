"""
Tests for reading text out of uploaded files.
"""

import io

import pytest
from docx import Document

from app.services.text_extraction import ResumeFileError, extract_text


def make_docx(text: str) -> bytes:
    document = Document()
    for line in text.split("\n"):
        document.add_paragraph(line)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_reads_a_docx():
    text = extract_text(make_docx("Built a React app for students. " * 10), "resume.docx")
    assert "React app" in text


def test_rejects_empty_files():
    with pytest.raises(ResumeFileError, match="empty"):
        extract_text(b"", "resume.pdf")


def test_rejects_other_file_types():
    with pytest.raises(ResumeFileError, match="PDF or DOCX"):
        extract_text(b"hello", "resume.png")


def test_rejects_files_with_almost_no_text():
    with pytest.raises(ResumeFileError, match="enough text"):
        extract_text(make_docx("Just a name"), "resume.docx")


def test_rejects_broken_pdfs():
    with pytest.raises(ResumeFileError):
        extract_text(b"not really a pdf", "resume.pdf")
