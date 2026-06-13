# 🎯 AI Resume ATS Scorer

An AI-powered Applicant Tracking System (ATS) resume analyzer that scores resumes, extracts insights, compares against job descriptions, and provides actionable feedback using NLP and LLMs.

🔗 **Live App:** [ai-resume-ats.streamlit.app](https://ai-resume-ats.streamlit.app)
🔗 **Backend API:** [ashharr-ats-backend.hf.space](https://ashharr-ats-backend.hf.space)

---

## ✨ Features

- 📄 **Resume Parsing** — Extracts text from PDF and DOCX resumes (with hyperlink detection)
- 🎯 **ATS Scoring** — Comprehensive scoring engine evaluating resume quality
- 🤖 **AI-Powered Feedback** — Personalized suggestions generated via Groq LLM
- 🔍 **JD Comparison** — Semantic similarity matching between resume and job description using Sentence Transformers
- 🧠 **NLP Analysis** — Keyword extraction, skill validation, and grammar checking powered by spaCy
- 📊 **History Tracking** — Stores past analyses per user
- 📥 **PDF Reports** — Downloadable analysis reports (via WeasyPrint)
- 🔐 **Authentication** — Secure email/password auth via Supabase

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| NLP | spaCy, Sentence Transformers |
| LLM | Groq API |
| Auth & DB | Supabase |
| File Parsing | pdfplumber, PyPDF2, python-docx |
| PDF Reports | WeasyPrint, Jinja2 |
| CI/CD | GitHub Actions |
| Hosting | Hugging Face Spaces (backend), Streamlit Cloud (frontend) |

---

## 📂 Project Structure

```
ai-resume-ats-main/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── core/
│   │   └── config.py            # App configuration & constants
│   ├── services/
│   │   ├── resume_parser.py     # File parsing & text extraction
│   │   ├── ats_scorer.py        # ATS scoring logic
│   │   ├── feedback_engine.py   # AI feedback generation
│   │   ├── groq_parser.py       # Groq LLM integration
│   │   ├── jd_matcher.py        # Job description comparison
│   │   ├── pdf_export.py        # PDF report generation
│   │   ├── recommendation_engine.py
│   │   ├── report_generator.py
│   │   └── resume_analyzer.py
│   └── utils/
│       └── file_utils.py        # Logging & error handling utilities
├── frontend/
│   ├── streamlit_app.py         # Streamlit app entrypoint
│   ├── services/
│   │   ├── api_client.py        # Backend API client
│   │   └── supabase_client.py   # Supabase auth client
│   ├── views/
│   │   ├── landing.py
│   │   ├── scorer.py
│   │   ├── history.py
│   │   └── resources.py
│   └── assets/
│       └── styles.css
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites
- Python 3.12
- A Supabase project (URL + anon key)
- A Groq API key

### 1. Clone the repository
```bash
git clone https://github.com/ashharkhan10/ai-resume-ats-system-.git
cd ai-resume-ats-system-
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the backend
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Run the frontend
```bash
streamlit run frontend/streamlit_app.py
```

The app will be available at `http://localhost:8501` and the backend at `http://localhost:8000`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/analyze-resume` | Analyze a resume and return ATS score & feedback |
| GET | `/api/v1/history` | Get user's analysis history |
| DELETE | `/api/v1/history/:id` | Delete a history entry |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/generate-pdf` | Generate a PDF report from analysis data |

---

## 🐳 Deployment

### Backend (Hugging Face Spaces)
The backend is containerized using Docker and deployed to Hugging Face Spaces.

Required secrets on HF Spaces:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `GROQ_API_KEY`

### Frontend (Streamlit Community Cloud)
Required secrets (`.streamlit/secrets.toml` or Streamlit Cloud Secrets):
```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_ANON_KEY = "your_supabase_anon_key"
AUTH_REDIRECT_URL = "https://ai-resume-ats.streamlit.app"
```

### CI/CD
GitHub Actions automatically runs tests on push. Deployment to Hugging Face Spaces is done via:
```bash
git push space main
```

---

## 🧩 Known Issues / Roadmap

- [ ] Google OAuth sign-in (PKCE flow incompatible with Streamlit reruns — currently disabled)
- [ ] TXT summary download is incomplete
- [x] PDF export (WeasyPrint) — fixed by adding GTK system dependencies in Docker

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋 Author

**Ashhar Khan**
GitHub: [@ashharkhan10](https://github.com/ashharkhan10)
