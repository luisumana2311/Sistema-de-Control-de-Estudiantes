from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("full_name_key", "section", name="uq_student_name_section"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    full_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    full_name_key: Mapped[str] = mapped_column(String(120), nullable=False)
    section: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
    grades: Mapped[list["Grade"]] = relationship(back_populates="student", cascade="all, delete-orphan", lazy="selectin")


class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = (
        UniqueConstraint("student_id", "subject", name="uq_grade_student_subject"),
        CheckConstraint("score >= 0 AND score <= 100", name="ck_grade_score_range"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    student: Mapped[Student] = relationship(back_populates="grades")
