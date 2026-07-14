import os
import unittest
from unittest.mock import patch

from src.student_control_system.database import get_database_url


class TestDatabaseConfiguration(unittest.TestCase):
    def test_converts_render_postgres_url_to_psycopg_driver(self):
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@db:5432/app"}):
            self.assertEqual(
                get_database_url(),
                "postgresql+psycopg://user:pass@db:5432/app",
            )

    def test_preserves_explicit_sqlalchemy_driver(self):
        url = "postgresql+psycopg://user:pass@db:5432/app"
        with patch.dict(os.environ, {"DATABASE_URL": url}):
            self.assertEqual(get_database_url(), url)
