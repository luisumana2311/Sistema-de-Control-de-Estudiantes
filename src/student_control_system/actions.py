import re


PASSING_GRADE = 60
MIN_GRADE = 0
MAX_GRADE = 100

SUBJECTS = (
    ("Spanish", "spanish_grade"),
    ("English", "english_grade"),
    ("Social Studies", "social_studies_grade"),
    ("Science", "science_grade"),
)

STUDENT_FIELDS = (
    "full_name",
    "section",
    *(field_name for _, field_name in SUBJECTS),
)

GRADE_FIELD_NAMES = tuple(field_name for _, field_name in SUBJECTS)


def is_valid_name(name):
    return bool(name.strip()) and not any(char.isdigit() for char in name)


def is_valid_section(section):
    pattern = r"^[0-9]{1,2}[A-Z]$"
    return re.match(pattern, section) is not None


def is_valid_grade(grade):
    return MIN_GRADE <= grade <= MAX_GRADE


def find_student(students, full_name, section):
    normalized_name = full_name.strip().lower()
    normalized_section = section.strip().upper()

    for student in students:
        if (
            student["full_name"].lower() == normalized_name
            and student["section"].upper() == normalized_section
        ):
            return student

    return None


def student_exists(students, full_name, section):
    return find_student(students, full_name, section) is not None


def search_students_by_name(students, search_term):
    normalized_search = search_term.strip().lower()

    if not normalized_search:
        return []

    return [
        student
        for student in students
        if normalized_search in student["full_name"].lower()
    ]


def update_student(student, full_name, section, grades):
    student["full_name"] = full_name
    student["section"] = section

    for field_name, grade in grades.items():
        if field_name in GRADE_FIELD_NAMES:
            student[field_name] = grade


def get_valid_name():
    while True:
        full_name = input("Enter full name: ").strip()

        if is_valid_name(full_name):
            return full_name

        print("Invalid name. It cannot be empty or contain numbers.")


def get_valid_section():
    while True:
        section = input("Enter section, for example 11B: ").strip().upper()

        if is_valid_section(section):
            return section

        print("Invalid section. Use a valid format like 10A, 11B or 12C.")


def get_valid_grade(subject):
    while True:
        try:
            grade = float(input(f"Enter {subject} grade: "))

            if is_valid_grade(grade):
                return grade

            print(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_confirmation(message):
    while True:
        confirmation = input(f"{message} (yes/no): ").strip().lower()

        if confirmation in ("yes", "y"):
            return True

        if confirmation in ("no", "n"):
            return False

        print("Invalid response. Please type 'yes' or 'no'.")


def calculate_average(student):
    total = sum(student[field_name] for _, field_name in SUBJECTS)
    return total / len(SUBJECTS)


def get_failed_subjects(student):
    failed_subjects = []

    for subject, field_name in SUBJECTS:
        grade = student[field_name]

        if grade < PASSING_GRADE:
            failed_subjects.append((subject, grade))

    return failed_subjects


def print_section_title(title):
    print(f"\n===== {title} =====")


def build_student_table(students, include_failed_subjects=False):
    headers = ["Name", "Section", "Spanish", "English", "Social", "Science", "Average"]
    rows = []

    for student in students:
        row = [
            student["full_name"],
            student["section"],
            f"{student['spanish_grade']:.2f}",
            f"{student['english_grade']:.2f}",
            f"{student['social_studies_grade']:.2f}",
            f"{student['science_grade']:.2f}",
            f"{calculate_average(student):.2f}",
        ]

        if include_failed_subjects:
            failed_subjects = get_failed_subjects(student)
            row.append(
                ", ".join(
                    f"{subject} ({grade:.2f})"
                    for subject, grade in failed_subjects
                )
            )

        rows.append(row)

    if include_failed_subjects:
        headers.append("Failed Subjects")

    widths = [
        max(len(str(row[column_index])) for row in [headers, *rows])
        for column_index in range(len(headers))
    ]

    lines = [
        " | ".join(
            str(header).ljust(widths[index])
            for index, header in enumerate(headers)
        ),
        "-+-".join("-" * width for width in widths),
    ]

    for row in rows:
        lines.append(
            " | ".join(
                str(value).ljust(widths[index])
                for index, value in enumerate(row)
            )
        )

    return "\n".join(lines)


def print_student_table(students, include_failed_subjects=False):
    print(build_student_table(students, include_failed_subjects))


def add_students(students):
    while True:
        try:
            amount = int(input("How many students do you want to add? ").strip())

            if amount > 0:
                break

            print("Amount must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    for index in range(amount):
        print(f"\nStudent #{index + 1}")

        full_name = get_valid_name()
        section = get_valid_section()

        if student_exists(students, full_name, section):
            print("This student already exists. Student was not added.")
            continue

        student = {
            "full_name": full_name,
            "section": section,
        }

        for subject, field_name in SUBJECTS:
            student[field_name] = get_valid_grade(subject)

        students.append(student)
        print("Student added successfully.")


def show_students(students):
    if not students:
        print("There are no students registered.")
        return

    print_section_title("Students List")
    print_student_table(students)


def show_top_three_students(students):
    if not students:
        print("There are no students registered.")
        return

    sorted_students = sorted(students, key=calculate_average, reverse=True)

    print_section_title("Top 3 Students")
    print_student_table(sorted_students[:3])


def show_general_average(students):
    if not students:
        print("There are no students registered.")
        return

    total_average = sum(calculate_average(student) for student in students)
    general_average = total_average / len(students)

    print_section_title("General Average")
    print(f"Registered students: {len(students)}")
    print(f"General average: {general_average:.2f}")


def delete_student(students):
    if not students:
        print("There are no students registered.")
        return

    full_name = input("Enter the full name of the student to delete: ").strip()
    section = input("Enter the section of the student: ").strip().upper()
    student = find_student(students, full_name, section)

    if student is None:
        print("Student not found.")
        return

    if get_confirmation(f"Are you sure you want to delete {full_name} from {section}?"):
        students.remove(student)
        print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")


def search_student(students):
    if not students:
        print("There are no students registered.")
        return

    search_term = input("Enter the name or part of the name to search: ").strip()
    results = search_students_by_name(students, search_term)

    if not search_term:
        print("Search term cannot be empty.")
        return

    if not results:
        print("No students matched your search.")
        return

    print_section_title("Search Results")
    print_student_table(results)


def edit_student(students):
    if not students:
        print("There are no students registered.")
        return

    full_name = input("Enter the full name of the student to edit: ").strip()
    section = input("Enter the section of the student: ").strip().upper()
    student = find_student(students, full_name, section)

    if student is None:
        print("Student not found.")
        return

    print("\nLeave a field empty to keep the current value.")
    new_full_name = input(f"Full name [{student['full_name']}]: ").strip()
    new_section = input(f"Section [{student['section']}]: ").strip().upper()

    updated_name = new_full_name or student["full_name"]
    updated_section = new_section or student["section"]

    if not is_valid_name(updated_name):
        print("Invalid name. Changes were not saved.")
        return

    if not is_valid_section(updated_section):
        print("Invalid section. Changes were not saved.")
        return

    duplicate_student = find_student(students, updated_name, updated_section)

    if duplicate_student is not None and duplicate_student is not student:
        print("Another student already exists with that name and section.")
        return

    updated_grades = {}

    for subject, field_name in SUBJECTS:
        current_grade = student[field_name]
        value = input(f"{subject} grade [{current_grade}]: ").strip()

        if not value:
            updated_grades[field_name] = current_grade
            continue

        try:
            grade = float(value)
        except ValueError:
            print(f"Invalid {subject} grade. Changes were not saved.")
            return

        if not is_valid_grade(grade):
            print(f"{subject} grade must be between {MIN_GRADE} and {MAX_GRADE}.")
            print("Changes were not saved.")
            return

        updated_grades[field_name] = grade

    update_student(student, updated_name, updated_section, updated_grades)
    print("Student updated successfully.")


def show_failed_students(students):
    if not students:
        print("There are no students registered.")
        return

    failed_students = [
        student for student in students if get_failed_subjects(student)
    ]

    if not failed_students:
        print("There are no failed students.")
        return

    print_section_title("Failed Students")
    print_student_table(failed_students, include_failed_subjects=True)
