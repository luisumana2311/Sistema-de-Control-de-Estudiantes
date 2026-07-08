import unittest
from unittest.mock import patch

from student_control_system.menu import get_menu_option


class TestMenu(unittest.TestCase):
    def test_get_menu_option_retries_until_valid_option(self):
        with patch("builtins.input", side_effect=["", "abc", "3"]):
            self.assertEqual(get_menu_option(), "3")


if __name__ == "__main__":
    unittest.main()
