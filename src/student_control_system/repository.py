from sqlalchemy import func, select

from .actions import SUBJECTS, is_valid_grade, is_valid_name, is_valid_section
from .models import Grade, Student


class StudentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, student_data):
        self._validate(student_data)
        student = Student(
            full_name=student_data["full_name"].strip(),
            section=student_data["section"].strip().upper(),
        )
        student.grades = [
            Grade(subject=field_name, score=float(student_data[field_name]))
            for _, field_name in SUBJECTS
        ]
        self.session.add(student)
        self.session.commit()
        return student

    def list_all(self):
        statement = select(Student).order_by(Student.section, Student.full_name)
        return list(self.session.scalars(statement).unique())

    def get(self, student_id):
        return self.session.get(Student, student_id)

    def find_by_name(self, search_term):
        term = search_term.strip().lower()
        if not term:
            return []
        statement = select(Student).where(func.lower(Student.full_name).contains(term)).order_by(Student.full_name)
        return list(self.session.scalars(statement).unique())

    def delete(self, student_id):
        student = self.get(student_id)
        if student is None:
            return False
        self.session.delete(student)
        self.session.commit()
        return True

    @staticmethod
    def to_dict(student):
        scores = {grade.subject: grade.score for grade in student.grades}
        return {"id": student.id, "full_name": student.full_name, "section": student.section, **scores}

    @staticmethod
    def _validate(student_data):
        if not is_valid_name(student_data.get("full_name", "")):
            raise ValueError("Invalid student name.")
        section = student_data.get("section", "").strip().upper()
        if not is_valid_section(section):
            raise ValueError("Invalid student section.")
        for subject, field_name in SUBJECTS:
            score = student_data.get(field_name)
            if not isinstance(score, (int, float)) or not is_valid_grade(score):
                raise ValueError(f"Invalid {subject} grade.")
