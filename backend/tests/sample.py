"""
A fake resume used by the tests, so no real AI call is needed.
"""

from app.schemas.resume import AIReading

SAMPLE_TEXT = """Priya Sharma
priya@example.com | +91 98765 43210 | github.com/priya
Computer science student who builds fast, accessible web apps with React and Node.js.
Looking for a frontend developer internship.
SKILLS React, JavaScript, Node.js, HTML, CSS, Docker
PROJECTS
Event Portal - Built a React and Node.js event portal used by 1200 students.
Improved page load time by 40% with code splitting.
Worked on a website for college events.
EDUCATION B.Tech Computer Science, Example University, 2026
""" + "Extra detail about coursework and activities. " * 40


def sample_reading(**target) -> AIReading:
    return AIReading.model_validate({
        "resume": {
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "phone": "+91 98765 43210",
            "summary": "Computer science student who builds fast, accessible web apps with React "
                       "and Node.js. Looking for a frontend developer internship.",
            "skills": ["React", "JavaScript", "Node.js", "HTML", "CSS", "Docker"],
            "projects": [{
                "title": "Event Portal",
                "technologies": ["React", "Node.js"],
                "bullets": [
                    "Built a React and Node.js event portal used by 1200 students.",
                    "Improved page load time by 40% with code splitting and lazy loading.",
                    "Worked on a website for college events.",
                ],
            }],
            "education": [{"degree": "B.Tech Computer Science", "institution": "Example University", "year": "2026"}],
        },
        "target": target or {},
        "rewrites": [{"before": "Worked on a website for college events.",
                      "after": "Built a college events site used by [N] students.", "why": "Adds impact"}],
        "strengths": ["Clear project with real users"],
    })
