import csv
import io

from sqlalchemy.exc import IntegrityError

from .actions import PASSING_GRADE, STUDENT_FIELDS, SUBJECTS, get_failed_subjects
from .data import build_student_from_row, validate_csv_headers
from .repository import StudentRepository
from .schemas import StudentResponse


class StudentService:
    def __init__(self, session):
        self.session = session
        self.repository = StudentRepository(session)

    @staticmethod
    def serialize(student):
        scores = {grade.subject: grade.score for grade in student.grades}
        average = sum(scores[field] for _, field in SUBJECTS) / len(SUBJECTS)
        return StudentResponse(
            id=student.id,
            full_name=student.full_name,
            section=student.section,
            average=round(average, 2),
            academic_status="passing" if average >= PASSING_GRADE else "at_risk",
            created_at=student.created_at,
            updated_at=student.updated_at,
            **scores,
        )

    def create(self, payload):
        return self.serialize(self.repository.create(payload))

    def update(self, student_id, payload):
        student = self.repository.update(student_id, payload)
        return self.serialize(student) if student else None

    def export_csv(self):
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=STUDENT_FIELDS)
        writer.writeheader()
        for student in self.repository.list_all(limit=100_000):
            data = self.repository.to_dict(student)
            writer.writerow({field: data[field] for field in STUDENT_FIELDS})
        return output.getvalue()

    def import_csv(self, content):
        text = content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        validate_csv_headers(reader.fieldnames)
        imported = 0
        skipped = 0
        errors = []
        for row_number, row in enumerate(reader, start=2):
            try:
                student_data = build_student_from_row(row, row_number)
                self.repository.create(student_data)
                imported += 1
            except IntegrityError:
                self.session.rollback()
                skipped += 1
            except (KeyError, TypeError, ValueError) as error:
                self.session.rollback()
                errors.append(str(error))
        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "message": f"Importación completada: {imported} creados, {skipped} duplicados omitidos.",
        }

    def failed_students(self):
        results = []
        for student in self.repository.students_with_failed_subjects():
            serialized = self.serialize(student).model_dump()
            results.append(
                serialized
                | {
                    "failed_subjects": [
                        {"subject": subject, "score": score}
                        for subject, score in get_failed_subjects(serialized)
                    ]
                }
            )
        return results
