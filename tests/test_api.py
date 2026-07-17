import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.student_control_system.api import app, get_session
from src.student_control_system.database import Base


VALID_STUDENT = {
    "full_name": "María Solano",
    "section": "10a",
    "spanish_grade": 92,
    "english_grade": 87,
    "social_studies_grade": 84,
    "science_grade": 95,
}


class TestStudentApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(cls.engine)
        cls.session_factory = sessionmaker(bind=cls.engine, autoflush=False, expire_on_commit=False)

        def override_session():
            session = cls.session_factory()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_session] = override_session
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        cls.engine.dispose()

    def setUp(self):
        with self.engine.begin() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                connection.execute(table.delete())

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_serves_professional_web_application(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("EduControl", response.text)

    def test_dashboard_returns_academic_summary(self):
        self.client.post("/api/v1/students", json=VALID_STUDENT)
        self.client.post("/api/v1/students", json={**VALID_STUDENT, "full_name": "Carlos Mora", "section": "11B", "spanish_grade": 40, "english_grade": 50, "social_studies_grade": 45, "science_grade": 55})
        response = self.client.get("/api/v1/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_students"], 2)
        self.assertEqual(response.json()["students_at_risk"], 1)
        self.assertEqual(len(response.json()["sections"]), 2)

    def test_complete_student_crud(self):
        create_response = self.client.post("/api/v1/students", json=VALID_STUDENT)
        self.assertEqual(create_response.status_code, 201)
        student = create_response.json()
        self.assertEqual(student["section"], "10A")
        self.assertEqual(student["average"], 89.5)

        get_response = self.client.get(f"/api/v1/students/{student['id']}")
        self.assertEqual(get_response.status_code, 200)

        updated_payload = {**VALID_STUDENT, "science_grade": 75}
        update_response = self.client.put(f"/api/v1/students/{student['id']}", json=updated_payload)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["science_grade"], 75)

        delete_response = self.client.delete(f"/api/v1/students/{student['id']}")
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(self.client.get(f"/api/v1/students/{student['id']}").status_code, 404)

    def test_lists_filters_and_paginates_students(self):
        self.client.post("/api/v1/students", json=VALID_STUDENT)
        self.client.post("/api/v1/students", json={**VALID_STUDENT, "full_name": "Luis Castro", "section": "11B"})
        response = self.client.get("/api/v1/students", params={"search": "maría", "section": "10A", "page_size": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 1)
        self.assertEqual(response.json()["items"][0]["full_name"], "María Solano")

    def test_rejects_duplicate_student(self):
        self.client.post("/api/v1/students", json=VALID_STUDENT)
        response = self.client.post("/api/v1/students", json={**VALID_STUDENT, "full_name": "MARÍA SOLANO"})
        self.assertEqual(response.status_code, 409)

    def test_validates_payload(self):
        response = self.client.post("/api/v1/students", json={**VALID_STUDENT, "science_grade": 120})
        self.assertEqual(response.status_code, 422)

    def test_top_failed_and_csv_endpoints(self):
        self.client.post("/api/v1/students", json=VALID_STUDENT)
        risk_student = {
            **VALID_STUDENT,
            "full_name": "Carlos Mora",
            "section": "11B",
            "spanish_grade": 40,
            "english_grade": 80,
        }
        self.client.post("/api/v1/students", json=risk_student)

        top = self.client.get("/api/v1/students/top")
        self.assertEqual(top.status_code, 200)
        self.assertEqual(top.json()[0]["full_name"], VALID_STUDENT["full_name"])

        failed = self.client.get("/api/v1/students/failed")
        self.assertEqual(failed.status_code, 200)
        self.assertEqual(failed.json()[0]["failed_subjects"][0]["subject"], "Spanish")

        exported = self.client.get("/api/v1/students/export")
        self.assertEqual(exported.status_code, 200)
        self.assertIn("full_name,section", exported.text)

        csv_content = (
            "full_name,section,spanish_grade,english_grade,"
            "social_studies_grade,science_grade\n"
            "Ana Rivera,12A,90,91,92,93\n"
        )
        imported = self.client.post(
            "/api/v1/students/import",
            files={"file": ("students.csv", csv_content, "text/csv")},
        )
        self.assertEqual(imported.status_code, 200)
        self.assertEqual(imported.json()["imported"], 1)

    def test_rejects_invalid_csv_file(self):
        response = self.client.post(
            "/api/v1/students/import",
            files={"file": ("students.txt", "invalid", "text/plain")},
        )
        self.assertEqual(response.status_code, 400)
