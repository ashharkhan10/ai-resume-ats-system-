"""
Entry point of the backend.

Creates the FastAPI app, allows the frontend to call it (CORS),
and plugs in the route files.

Run it with:
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_URLS
from app.database import init_db
from app.routes import analyses, analyze, auth, health, share


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()  # create the tables on first start
    yield


app = FastAPI(title="AI Resume ATS API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(auth.router)
app.include_router(analyses.router)
app.include_router(share.router)
