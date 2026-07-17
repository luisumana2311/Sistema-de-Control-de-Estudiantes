import unittest
from unittest.mock import patch

from student_control_system.actions import (
    build_student_table,
    calculate_average,
    get_confirmation,
    find_student,
    get_failed_subjects,
    is_valid_grade,
    is_valid_name,
    is_valid_section,
    search_students_by_name,
    student_exists,
    update_student,
)


class TestActions(unittest.TestCase):
    def setUp(self):
        self.student = {
            "full_name": "Maria Lopez",
            "section": "11B",
            "spanish_grade": 95.0,
            "english_grade": 85.0,
            "social_studies_grade": 70.0,
            "science_grade": 50.0,
        }

    def test_validates_name(self):
        self.assertTrue(is_valid_name("Maria Lopez"))
        self.assertTrue(is_valid_name("María O'Connor-Solano"))
        self.assertFalse(is_valid_name(""))
        self.assertFalse(is_valid_name("Maria 123"))
        self.assertFalse(is_valid_name("=2+2"))

    def test_validates_section(self):
        self.assertTrue(is_valid_section("11B"))
        self.assertFalse(is_valid_section("B11"))
        self.assertFalse(is_valid_section("111B"))

    def test_validates_grade_range(self):
        self.assertTrue(is_valid_grade(0))
        self.assertTrue(is_valid_grade(100))
        self.assertFalse(is_valid_grade(-1))
        self.assertFalse(is_valid_grade(101))

    def test_calculates_average(self):
        self.assertEqual(calculate_average(self.student), 75.0)

    def test_get_failed_subjects(self):
        self.assertEqual(get_failed_subjects(self.student), [("Science", 50.0)])

    def test_student_exists_is_case_insensitive(self):
        students = [self.student]

        self.assertTrue(student_exists(students, "maria lopez", "11b"))
        self.assertFalse(student_exists(students, "Maria Lopez", "10A"))

    def test_finds_student_by_name_and_section(self):
        students = [self.student]

        self.assertIs(find_student(students, " maria lopez ", "11b"), self.student)
        self.assertIsNone(find_student(students, "Maria Lopez", "10A"))

    def test_searches_students_by_partial_name(self):
        students = [
            self.student,
            {
                "full_name": "Carlos Mora",
                "section": "10A",
                "spanish_grade": 80.0,
                "english_grade": 82.0,
                "social_studies_grade": 84.0,
                "science_grade": 86.0,
            },
        ]

        self.assertEqual(search_students_by_name(students, "maria"), [self.student])
        self.assertEqual(search_students_by_name(students, "lopez"), [self.student])
        self.assertEqual(search_students_by_name(students, ""), [])

    def test_updates_student(self):
        update_student(
            self.student,
            "Maria Fernandez",
            "12C",
            {
                "spanish_grade": 100.0,
                "unknown_field": 0.0,
            },
        )

        self.assertEqual(self.student["full_name"], "Maria Fernandez")
        self.assertEqual(self.student["section"], "12C")
        self.assertEqual(self.student["spanish_grade"], 100.0)
        self.assertNotIn("unknown_field", self.student)

    def test_builds_student_table(self):
        table = build_student_table([self.student])

        self.assertIn("Name", table)
        self.assertIn("Maria Lopez", table)
        self.assertIn("75.00", table)

    def test_confirmation_accepts_short_answers(self):
        with patch("builtins.input", side_effect=["y"]):
            self.assertTrue(get_confirmation("Continue?"))

        with patch("builtins.input", side_effect=["n"]):
            self.assertFalse(get_confirmation("Continue?"))


if __name__ == "__main__":
    unittest.main()
