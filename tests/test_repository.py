import unittest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from src.student_control_system.database import Base, build_session_factory
from src.student_control_system.repository import StudentRepository


STUDENT = {
    "full_name": "Ana Rivera",
    "section": "11A",
    "spanish_grade": 90,
    "english_grade": 85,
    "social_studies_grade": 88,
    "science_grade": 92,
}


class TestStudentRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = build_session_factory(self.engine)()
        self.repository = StudentRepository(self.session)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_creates_and_reads_student_with_grades(self):
        created = self.repository.create(STUDENT)
        stored = self.repository.get(created.id)
        result = self.repository.to_dict(stored)
        self.assertEqual(result["full_name"], "Ana Rivera")
        self.assertEqual(result["science_grade"], 92)
        self.assertEqual(len(stored.grades), 4)

    def test_searches_students_case_insensitively(self):
        self.repository.create(STUDENT)
        self.assertEqual(len(self.repository.find_by_name("ana")), 1)

    def test_rejects_duplicate_name_and_section(self):
        self.repository.create(STUDENT)
        with self.assertRaises(IntegrityError):
            self.repository.create({**STUDENT, "full_name": "ANA RIVERA", "section": "11a"})
        self.session.rollback()

    def test_deletes_student_and_cascades_grades(self):
        created = self.repository.create(STUDENT)
        self.assertTrue(self.repository.delete(created.id))
        self.assertIsNone(self.repository.get(created.id))

    def test_validates_data_before_persisting(self):
        invalid = {**STUDENT, "science_grade": 101}
        with self.assertRaisesRegex(ValueError, "Science"):
            self.repository.create(invalid)
