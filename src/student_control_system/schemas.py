from datetime import datetime

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .actions import is_valid_name


class StudentPayload(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    section: str = Field(pattern=r"^[0-9]{1,2}[A-Za-z]$")
    spanish_grade: float = Field(ge=0, le=100)
    english_grade: float = Field(ge=0, le=100)
    social_studies_grade: float = Field(ge=0, le=100)
    science_grade: float = Field(ge=0, le=100)

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):
        clean = " ".join(value.split())
        if not is_valid_name(clean):
            raise ValueError(
                "El nombre solo puede contener letras, espacios, apóstrofes y guiones."
            )
        return clean

    @field_validator("section")
    @classmethod
    def normalize_section(cls, value):
        return value.upper()


class StudentResponse(StudentPayload):
    model_config = ConfigDict(from_attributes=True)
    id: str
    average: float
    academic_status: Literal["passing", "at_risk"]
    created_at: datetime
    updated_at: datetime


class StudentListResponse(BaseModel):
    items: list[StudentResponse]
    total: int
    page: int
    page_size: int


class ImportResult(BaseModel):
    imported: int
    skipped: int
    errors: list[str]
    message: str


class FailedSubject(BaseModel):
    subject: str
    score: float


class FailedStudentResponse(StudentResponse):
    failed_subjects: list[FailedSubject]
