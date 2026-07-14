from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .actions import PASSING_GRADE, SUBJECTS
from .database import build_engine, build_session_factory
from .repository import StudentRepository
from .schemas import StudentListResponse, StudentPayload, StudentResponse


engine = build_engine(pool_pre_ping=True)
SessionFactory = build_session_factory(engine)
app = FastAPI(title="Student Control System API", version="2.0.0", description="REST API for student records, grades and academic indicators.")
WEB_DIR = Path(__file__).resolve().parent / "web"
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


def serialize_student(student):
    scores = {grade.subject: grade.score for grade in student.grades}
    average = sum(scores[field] for _, field in SUBJECTS) / len(SUBJECTS)
    return StudentResponse(id=student.id, full_name=student.full_name, section=student.section, average=round(average, 2), academic_status="passing" if average >= PASSING_GRADE else "at_risk", created_at=student.created_at, updated_at=student.updated_at, **scores)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def web_app():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/v1/dashboard", tags=["Dashboard"])
def dashboard(session: Session = Depends(get_session)):
    return StudentRepository(session).academic_summary()


@app.get("/api/v1/students", response_model=StudentListResponse, tags=["Students"])
def list_students(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), search: str | None = Query(None, max_length=120), section: str | None = Query(None, pattern=r"^[0-9]{1,2}[A-Za-z]$"), session: Session = Depends(get_session)):
    repository = StudentRepository(session)
    students = repository.list_all(offset=(page - 1) * page_size, limit=page_size, search=search, section=section)
    return StudentListResponse(items=[serialize_student(student) for student in students], total=repository.count(search=search, section=section), page=page, page_size=page_size)


@app.get("/api/v1/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def get_student(student_id: str, session: Session = Depends(get_session)):
    student = StudentRepository(session).get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return serialize_student(student)


@app.post("/api/v1/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(payload: StudentPayload, session: Session = Depends(get_session)):
    try:
        student = StudentRepository(session).create(payload.model_dump())
        return serialize_student(student)
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(status_code=409, detail="A student with this name and section already exists.") from error


@app.put("/api/v1/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def update_student(student_id: str, payload: StudentPayload, session: Session = Depends(get_session)):
    try:
        student = StudentRepository(session).update(student_id, payload.model_dump())
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found.")
        return serialize_student(student)
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(status_code=409, detail="A student with this name and section already exists.") from error


@app.delete("/api/v1/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: str, session: Session = Depends(get_session)):
    if not StudentRepository(session).delete(student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
