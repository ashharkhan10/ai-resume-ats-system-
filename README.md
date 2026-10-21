# AI Resume ATS

**Check your resume like an applicant tracking system does — then fix it with AI.**
Built for students and fresh graduates.

🔗 **Live:** https://ai-resume-ats.vercel.app  ·  **API:** https://ashharr-ats-backend.hf.space/docs

---

## Features

| | |
|---|---|
| 📊 **ATS score** | One score out of 100 from 5 categories: keywords, content, formatting, skill proof, ATS-friendliness |
| 🎯 **Job match** | Paste a job description — see matched and missing keywords |
| 🧭 **Target role mode** | No job post? Pick one of 16 roles (Frontend, Data Analyst, ML Engineer, …) |
| ✍️ **AI bullet rewriter** | Weak bullets rewritten with strong verbs and measurable results |
| 💬 **Interview prep** | Likely questions made from *your* projects, with tips on answering |
| ✉️ **Cover letter** | Tailored letter in 3 tones — edit and copy |
| 📈 **Version tracking** | Every check is saved; see your score trend and compare two versions |
| 🔗 **Share link** | Send a read-only report to a mentor or friend |
| ⬇️ **PDF download** | Save the full report as a PDF |
| 🔐 **Accounts** | Email + password login (JWT, Argon2 hashing) |

## Tech stack

- **Frontend:** Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, Vitest — on **Vercel**
- **Backend:** FastAPI, Pydantic v2, SQLAlchemy, pytest — on **Hugging Face Spaces** (Docker)
- **Database:** PostgreSQL on **Supabase** (JSONB for saved reports)
- **AI:** Groq (`openai/gpt-oss-120b`)
- **CI/CD:** GitHub Actions — tests both apps, then deploys the backend

## How it works

```
Browser (Next.js) ──► POST /analyze ──► 1. extract text (pypdf / python-docx)
                                         2. ONE AI call: read the resume + the job's skills, write rewrites
                                         3. score it with plain Python (fast, same result every time)
                                         4. save the report ──► PostgreSQL
```

The AI only *reads* the resume. All scoring is deterministic Python, so it's fast, testable and fair.
The old version made several slow calls and loaded heavy NLP models; this one makes a single call.

| Category | Weight | What it checks |
|---|---|---|
| Keywords | 30 | Required (×2) and preferred skills from the job found in the resume |
| Content | 25 | Bullets with numbers, strong action verbs, good length |
| Formatting | 15 | Contact details, summary, skills, experience/projects, education |
| Skill proof | 15 | Skills actually used in a project or job, not just listed |
| ATS friendly | 15 | Length, odd characters, readable email, real bullet points |

## Project structure

```
ai-resume-ats/
├── backend/                 FastAPI app
│   ├── app/
│   │   ├── routes/          analyze, auth, analyses (versions, interview, cover letter), share
│   │   ├── services/        text extraction, AI reader, scoring/, issues, interview, cover letter
│   │   ├── schemas/         request & response shapes
│   │   ├── models.py        database tables
│   │   └── main.py          app entry point
│   ├── tests/               pytest (no real AI calls)
│   └── Dockerfile           for Hugging Face Spaces
├── frontend/                Next.js app
│   └── src/
│       ├── app/             pages: /, /analyze, /report/[id], /share/[id], /versions, /login, /register
│       ├── components/      landing, analyze, results, versions, auth, layout, ui
│       └── lib/             api client, auth, helpers (+ tests)
└── github/workflows/ci.yml  move to .github/workflows/ (see below)
```

## Run it locally

**Backend** (Python 3.12)

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env           # then add your GROQ_API_KEY
pytest
uvicorn app.main:app --reload    # http://127.0.0.1:8000/docs
```

Without `DATABASE_URL` the backend uses a local SQLite file, so no database setup is needed to try it.

**Frontend** (Node 22)

```bash
cd frontend
npm install
npm test
npm run dev                      # http://localhost:3000
```

## Environment variables

| Where | Name | What |
|---|---|---|
| Backend | `GROQ_API_KEY` | Groq API key |
| Backend | `DATABASE_URL` | Supabase PostgreSQL URL (session pooler) |
| Backend | `JWT_SECRET` | long random text for login tokens |
| Backend | `FRONTEND_URL` | site(s) allowed to call the API, comma-separated |
| Frontend | `NEXT_PUBLIC_API_URL` | backend address |

## Old version

The first version was a Streamlit app. `frontend/streamlit_app.py` now only redirects
the old link (ai-resume-ats.streamlit.app) to the new site.
