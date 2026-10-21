"""
Section headings — the way a real ATS finds them.

ATS software splits a resume by its headings. Standard names ("Experience",
"Education", "Skills") are found reliably; creative ones ("My Journey") often aren't.
"""

import re
from dataclasses import dataclass, field

# Standard section → headings an ATS recognises for it
STANDARD_SECTIONS = {
    "Experience": ["experience", "work experience", "professional experience", "employment",
                   "work history", "internships", "internship", "internship experience"],
    "Education": ["education", "academic background", "academics", "qualifications",
                  "educational qualifications"],
    "Skills": ["skills", "technical skills", "core skills", "key skills", "skills & tools",
               "skills and tools", "technologies", "tech stack", "core competencies"],
    "Projects": ["projects", "academic projects", "personal projects", "key projects"],
    "Summary": ["summary", "professional summary", "profile", "objective", "career objective",
                "about", "about me"],
    "Certifications": ["certifications", "certificates", "licenses & certifications",
                       "courses", "achievements", "awards"],
}

# Every resume should have these (Experience OR Projects counts as "work")
MUST_HAVE = ["Education", "Skills"]

# Headings that look nice to people but confuse ATS software
CREATIVE_HEADINGS = ["my journey", "my story", "where i've been", "what i do", "what i've done",
                     "my toolbox", "toolbox", "things i've built", "stuff i've built",
                     "career journey", "my work", "superpowers", "who am i"]

# A heading is a short line: up to 5 words, mostly letters
HEADING_LINE = re.compile(r"^[A-Za-z&/' ]{3,40}:?$")


@dataclass
class SectionCheck:
    found: list[str] = field(default_factory=list)  # standard sections that were found
    missing: list[str] = field(default_factory=list)  # must-have sections that weren't
    creative: list[str] = field(default_factory=list)  # creative headings that were used


def _heading_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip().rstrip(":").strip()
        if line and len(line.split()) <= 5 and HEADING_LINE.match(line):
            lines.append(line.lower())
    return lines


def detect_sections(text: str) -> SectionCheck:
    headings = _heading_lines(text)
    found = [name for name, options in STANDARD_SECTIONS.items() if any(h in options for h in headings)]

    missing = [name for name in MUST_HAVE if name not in found]
    if "Experience" not in found and "Projects" not in found:
        missing.insert(0, "Experience or Projects")

    creative = sorted({h for h in headings if h in CREATIVE_HEADINGS})
    return SectionCheck(found=found, missing=missing, creative=[c.title() for c in creative])
