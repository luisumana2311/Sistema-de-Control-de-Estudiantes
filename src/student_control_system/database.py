import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://student_app:student_app@localhost:5432/student_control"
)


class Base(DeclarativeBase):
    pass


def get_database_url():
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def build_engine(database_url=None, **kwargs):
    return create_engine(database_url or get_database_url(), **kwargs)


def build_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
