import unittest

from actions import (
    calculate_average,
    get_failed_subjects,
    is_valid_grade,
    is_valid_name,
    is_valid_section,
    student_exists,
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
        self.assertFalse(is_valid_name(""))
        self.assertFalse(is_valid_name("Maria 123"))

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


if __name__ == "__main__":
    unittest.main()
