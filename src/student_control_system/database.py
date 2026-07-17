import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from . import config  # noqa: F401 - carga .env antes de leer DATABASE_URL

DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://student_app:student_app@localhost:5432/student_control"
)


class Base(DeclarativeBase):
    pass


def get_database_url():
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def build_engine(database_url=None, **kwargs):
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
