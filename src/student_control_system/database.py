import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from . import config  # noqa: F401 - carga .env antes de leer DATABASE_URL

DEFAULT_DATABASE_URL = "sqlite:///./student_control.db"


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        if os.getenv("RAILWAY_ENVIRONMENT"):
            raise RuntimeError("DATABASE_URL is required in Railway.")
        return DEFAULT_DATABASE_URL

    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def build_engine(database_url: str | None = None, **kwargs: Any):
    url = database_url or get_database_url()
    if url.startswith("sqlite"):
        kwargs.setdefault("connect_args", {"check_same_thread": False})
    return create_engine(url, **kwargs)


def build_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


engine = build_engine(pool_pre_ping=True)
SessionFactory = build_session_factory(engine)


def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
