from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from student_control_system.menu import show_menu


def main():
    students = []
    show_menu(students)


if __name__ == "__main__":
    main()
