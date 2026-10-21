"""
Database connection.

get_db() gives each request its own session and closes it afterwards.
init_db() creates the tables if they don't exist yet.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import DATABASE_URL


def _make_engine(url: str):
    # Supabase gives "postgresql://…" — tell SQLAlchemy to use the psycopg driver.
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    if url.startswith("sqlite"):
        options = {"connect_args": {"check_same_thread": False}}
        if url == "sqlite://":  # in-memory database for tests
            options["poolclass"] = StaticPool
        return create_engine(url, **options)

    return create_engine(url, pool_pre_ping=True, connect_args={"prepare_threshold": None})


engine = _make_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app import models  # noqa: F401  (registers the tables)

    Base.metadata.create_all(engine)
    print(f"Database ready: {engine.url.get_backend_name()}")
