from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_session
from ..repository import StudentRepository
from ..schemas import ImportResult, StudentListResponse, StudentPayload, StudentResponse
from ..services import StudentService


router = APIRouter(prefix="/api/v1", tags=["Students"])


@router.get("/dashboard", tags=["Dashboard"])
def dashboard(session: Session = Depends(get_session)):
    return StudentRepository(session).academic_summary()


@router.get("/students", response_model=StudentListResponse)
def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, max_length=120),
    section: str | None = Query(None, pattern=r"^[0-9]{1,2}[A-Za-z]$"),
    session: Session = Depends(get_session),
):
    repository = StudentRepository(session)
    service = StudentService(session)
    students = repository.list_all(
        offset=(page - 1) * page_size,
        limit=page_size,
        search=search,
        section=section,
    )
    return StudentListResponse(
        items=[service.serialize(student) for student in students],
        total=repository.count(search=search, section=section),
        page=page,
        page_size=page_size,
    )


@router.get("/students/top", response_model=list[StudentResponse])
def top_students(session: Session = Depends(get_session)):
    service = StudentService(session)
    return [service.serialize(item) for item in service.repository.top_students()]


@router.get("/students/failed")
def failed_students(session: Session = Depends(get_session)):
    return StudentService(session).failed_students()


@router.get("/students/export")
def export_students(session: Session = Depends(get_session)):
    csv_text = StudentService(session).export_csv()
    return StreamingResponse(
        iter([csv_text]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="estudiantes.csv"'},
    )


@router.post("/students/import", response_model=ImportResult)
async def import_students(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Selecciona un archivo CSV válido.")
    content = await file.read()
    if len(content) > 2_000_000:
        raise HTTPException(status_code=413, detail="El archivo supera el límite de 2 MB.")
    try:
        return StudentService(session).import_csv(content)
    except (UnicodeDecodeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, session: Session = Depends(get_session)):
    student = StudentRepository(session).get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return StudentService.serialize(student)


@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(payload: StudentPayload, session: Session = Depends(get_session)):
    try:
        return StudentService(session).create(payload.model_dump())
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un estudiante con este nombre y sección.",
        ) from error


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    payload: StudentPayload,
    session: Session = Depends(get_session),
):
    try:
        student = StudentService(session).update(student_id, payload.model_dump())
        if student is None:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
        return student
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un estudiante con este nombre y sección.",
        ) from error


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, session: Session = Depends(get_session)):
    if not StudentRepository(session).delete(student_id):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
