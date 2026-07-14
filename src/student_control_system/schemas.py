from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
        if any(character.isdigit() for character in clean):
            raise ValueError("Name cannot contain numbers.")
        return clean

    @field_validator("section")
    @classmethod
    def normalize_section(cls, value):
        return value.upper()


class StudentResponse(StudentPayload):
    model_config = ConfigDict(from_attributes=True)
    id: str
    average: float
    academic_status: str
    created_at: datetime
    updated_at: datetime


class StudentListResponse(BaseModel):
    items: list[StudentResponse]
    total: int
    page: int
    page_size: int
