from sqlalchemy import case, func, select

from .actions import SUBJECTS, is_valid_grade, is_valid_name, is_valid_section
from .models import Grade, Student


class StudentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, student_data):
        self._validate(student_data)
        student = Student(
            full_name=student_data["full_name"].strip(),
            full_name_key=student_data["full_name"].strip().casefold(),
            section=student_data["section"].strip().upper(),
        )
        student.grades = [
            Grade(subject=field_name, score=float(student_data[field_name]))
            for _, field_name in SUBJECTS
        ]
        self.session.add(student)
        self.session.commit()
        return student

    def list_all(self, offset=0, limit=50, search=None, section=None):
        statement = select(Student)
        if search:
            statement = statement.where(func.lower(Student.full_name).contains(search.strip().lower()))
        if section:
            statement = statement.where(func.upper(Student.section) == section.strip().upper())
        statement = statement.order_by(Student.section, Student.full_name).offset(offset).limit(limit)
        return list(self.session.scalars(statement).unique())

    def count(self, search=None, section=None):
        statement = select(func.count()).select_from(Student)
        if search:
            statement = statement.where(func.lower(Student.full_name).contains(search.strip().lower()))
        if section:
            statement = statement.where(func.upper(Student.section) == section.strip().upper())
        return self.session.scalar(statement) or 0

    def academic_summary(self):
        student_averages = (
            select(Grade.student_id, func.avg(Grade.score).label("average"))
            .group_by(Grade.student_id)
            .subquery()
        )
        overview = self.session.execute(
            select(
                func.count(Student.id),
                func.coalesce(func.avg(student_averages.c.average), 0),
                func.coalesce(func.sum(case((student_averages.c.average < 60, 1), else_=0)), 0),
            ).outerjoin(student_averages, Student.id == student_averages.c.student_id)
        ).one()
        sections = self.session.execute(
            select(Student.section, func.count(Student.id))
            .group_by(Student.section)
            .order_by(Student.section)
        ).all()
        return {
            "total_students": overview[0],
            "general_average": round(float(overview[1]), 2),
            "students_at_risk": overview[2],
            "passing_students": overview[0] - overview[2],
            "sections": [{"section": section, "total": total} for section, total in sections],
        }

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

    def update(self, student_id, student_data):
        self._validate(student_data)
        student = self.get(student_id)
        if student is None:
            return None
        student.full_name = student_data["full_name"].strip()
        student.full_name_key = student.full_name.casefold()
        student.section = student_data["section"].strip().upper()
        grades = {grade.subject: grade for grade in student.grades}
        for _, field_name in SUBJECTS:
            grades[field_name].score = float(student_data[field_name])
        self.session.commit()
        return student

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
