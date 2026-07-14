import csv
import os
import tempfile
import unittest
from unittest.mock import patch

from student_control_system import data


class TestData(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "students.csv")
        self.file_name_patch = patch.object(data, "FILE_NAME", self.csv_path)
        self.file_name_patch.start()

    def tearDown(self):
        self.file_name_patch.stop()
        self.temp_dir.cleanup()

    def write_csv(self, rows, fieldnames=None):
        fieldnames = fieldnames or data.STUDENT_FIELDS

        with open(self.csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_export_and_import_students(self):
        students = [
            {
                "full_name": "Maria Lopez",
                "section": "11B",
                "spanish_grade": 95.0,
                "english_grade": 85.0,
                "social_studies_grade": 70.0,
                "science_grade": 50.0,
            }
        ]

        data.export_to_csv(students)

        self.assertEqual(data.import_from_csv(), students)

    def test_import_rejects_missing_required_columns(self):
        self.write_csv(
            [{"full_name": "Maria Lopez", "section": "11B"}],
            fieldnames=["full_name", "section"],
        )

        self.assertIsNone(data.import_from_csv())

    def test_import_rejects_grade_outside_valid_range(self):
        self.write_csv(
            [
                {
                    "full_name": "Maria Lopez",
                    "section": "11B",
                    "spanish_grade": 95.0,
                    "english_grade": 85.0,
                    "social_studies_grade": 70.0,
                    "science_grade": 150.0,
                }
            ]
        )

        self.assertIsNone(data.import_from_csv())


if __name__ == "__main__":
    unittest.main()
