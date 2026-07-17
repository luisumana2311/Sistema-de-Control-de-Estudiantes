import os
import unittest
from unittest.mock import patch

from src.student_control_system.database import get_database_url


class TestDatabaseConfiguration(unittest.TestCase):
    def test_normalizes_railway_postgresql_url_for_psycopg(self):
        with patch.dict(
            os.environ,
            {"DATABASE_URL": "postgresql://user:secret@host/database"},
            clear=False,
        ):
            self.assertEqual(
                get_database_url(),
                "postgresql+psycopg://user:secret@host/database",
            )

    def test_requires_database_url_in_railway(self):
        environment = {"RAILWAY_ENVIRONMENT": "production"}
        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaisesRegex(RuntimeError, "DATABASE_URL"):
                get_database_url()

    def test_uses_sqlite_for_local_development(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_database_url(), "sqlite:///./student_control.db")
