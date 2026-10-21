"""
All settings for the backend live here.
Values are read from the .env file, so secrets never go inside the code.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# The address(es) of the frontend. Only these sites may call the backend.
# Several can be given, separated by commas.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
FRONTEND_URLS = [url.strip().rstrip("/") for url in FRONTEND_URL.split(",") if url.strip()]

# Groq AI
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Database. Locally a small SQLite file is used if DATABASE_URL is empty.
# In production this is the Supabase PostgreSQL URL.
DATABASE_URL = os.getenv("DATABASE_URL", "") or "sqlite:///./local.db"

# Login tokens
JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-secret-change-me")
TOKEN_DAYS = 7

# Uploads
MAX_FILE_MB = 5
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
