"""
Layout check: things in the FILE that make ATS software misread a resume.

  - two-column layouts (text from both columns gets mixed together)
  - tables and text boxes (often skipped)
  - images / icons (can't be read at all)
  - contact details in the page header/footer (many ATS ignore these areas)

This never raises: if a check can't run, that item is simply left as "unknown".
"""

import io
import re
from dataclasses import dataclass

from docx import Document
from pypdf import PdfReader

CONTACT = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\+?\d[\d\s().-]{8,}\d")
DATE_LIKE = re.compile(r"\b(19|20)\d{2}\b|present|current", re.IGNORECASE)

# A gap of this many spaces inside a line = text sitting side by side
COLUMN_GAP = re.compile(r"\S(\s{8,})\S")
# Two-column if at least this share of lines (and this many lines) have side-by-side text
COLUMN_LINE_SHARE = 0.25
COLUMN_MIN_LINES = 8


@dataclass
class LayoutInfo:
    two_columns: bool | None = None
    tables: int | None = None
    text_boxes: bool | None = None
    images: int | None = None
    contact_in_header: bool | None = None


def inspect_layout(file_bytes: bytes, filename: str) -> LayoutInfo:
    try:
        if filename.lower().endswith(".pdf"):
            return _inspect_pdf(file_bytes)
        if filename.lower().endswith(".docx"):
            return _inspect_docx(file_bytes)
    except Exception as error:  # a broken file shouldn't stop the analysis
        print(f"Layout check skipped: {error}")
    return LayoutInfo()


# ---------- PDF ----------

def _inspect_pdf(file_bytes: bytes) -> LayoutInfo:
    reader = PdfReader(io.BytesIO(file_bytes))
    info = LayoutInfo()

    lines: list[str] = []
    images = 0
    for page in reader.pages:
        try:
            lines += [l for l in page.extract_text(extraction_mode="layout").splitlines() if l.strip()]
        except Exception:
            pass
        try:
            images += len(page.images)
        except Exception:
            pass

    info.images = images
    if lines:
        side_by_side = sum(1 for line in lines if _looks_like_two_columns(line))
        info.two_columns = side_by_side >= COLUMN_MIN_LINES and side_by_side / len(lines) >= COLUMN_LINE_SHARE
    return info


def _looks_like_two_columns(line: str) -> bool:
    """True if the line has real text on both sides of a big gap (not just a right-aligned date)."""
    match = COLUMN_GAP.search(line)
    if not match:
        return False
    left, right = line[: match.start(1)].strip(), line[match.end(1):].strip()
    if DATE_LIKE.search(right) or DATE_LIKE.search(left[-12:]):
        return False
    return len(re.findall(r"[A-Za-z]{2,}", left)) >= 2 and len(re.findall(r"[A-Za-z]{2,}", right)) >= 2


# ---------- DOCX ----------

def _inspect_docx(file_bytes: bytes) -> LayoutInfo:
    document = Document(io.BytesIO(file_bytes))
    body_xml = document.element.xml

    header_text = ""
    for section in document.sections:
        for part in (section.header, section.footer):
            header_text += " ".join(p.text for p in part.paragraphs)

    return LayoutInfo(
        two_columns=bool(re.search(r'<w:cols[^>]*w:num="([2-9])"', body_xml)),
        tables=len(document.tables),
        text_boxes="txbxContent" in body_xml,
        images=body_xml.count("<w:drawing") + body_xml.count("<w:pict"),
        contact_in_header=bool(CONTACT.search(header_text)),
    )
