import unittest

from sqlalchemy import create_engine

from src.student_control_system.database import Base, build_session_factory
from src.student_control_system.demo_data import seed_demo_data
from src.student_control_system.repository import StudentRepository


class TestDemoData(unittest.TestCase):
    def test_seed_is_idempotent(self):
        engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(engine)
        session = build_session_factory(engine)()
        try:
            self.assertEqual(seed_demo_data(session), (10, 0))
            self.assertEqual(seed_demo_data(session), (0, 10))
            self.assertEqual(StudentRepository(session).count(), 10)
        finally:
            session.close()
            engine.dispose()
