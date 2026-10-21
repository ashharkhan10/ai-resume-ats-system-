"""
The "Can an ATS read your resume?" checklist shown in the report.
"""

from app.schemas.analysis import Check
from app.services.layout_check import LayoutInfo
from app.services.scoring.ats_friendly import EMAIL_PATTERN, ODD_CHARACTERS
from app.services.sections import SectionCheck

ODD_CHARACTER_LIMIT = 5


def build_ats_checks(text: str, layout: LayoutInfo, sections: SectionCheck) -> list[Check]:
    def check(id: str, label: str, ok: bool | None, good: str, bad: str) -> Check:
        detail = "" if ok is None else (good if ok else bad)
        return Check(id=id, label=label, ok=ok, detail=detail)

    found = ", ".join(sections.found) or "none"
    odd = len(ODD_CHARACTERS.findall(text))

    return [
        check("sections", "Standard section headings", not sections.missing,
              f"Found: {found}.", f"Missing: {', '.join(sections.missing)}. Use plain headings like 'Education'."),
        check("creative", "No creative headings", not sections.creative,
              "Headings are easy to recognise.",
              f"'{', '.join(sections.creative)}' may not be recognised. Rename to standard headings."),
        check("columns", "Single-column layout", None if layout.two_columns is None else not layout.two_columns,
              "Text reads top to bottom.", "Two columns can get mixed up. Use one column."),
        check("tables", "No tables", None if layout.tables is None else layout.tables == 0,
              "No tables found.", f"{layout.tables} table(s) found — some ATS skip table text."),
        check("text_boxes", "No text boxes", None if layout.text_boxes is None else not layout.text_boxes,
              "No text boxes found.", "Text boxes are often skipped. Move the text into the page."),
        check("images", "No images or icons", None if layout.images is None else layout.images == 0,
              "No images found.", f"{layout.images} image(s)/icon(s) — an ATS can't read them."),
        check("header", "Contact details in the page body",
              None if layout.contact_in_header is None else not layout.contact_in_header,
              "Contact details are readable.", "Your contact details are in the page header/footer, which many ATS ignore."),
        check("email", "Email address readable", bool(EMAIL_PATTERN.search(text)),
              "Email found.", "No email found in the text. Write it in plain text, not as an icon."),
        check("symbols", "Clean text (no odd symbols)", odd <= ODD_CHARACTER_LIMIT,
              "Text extracted cleanly.", f"{odd} unusual symbols found — often from icons, tables or fancy bullets."),
    ]
