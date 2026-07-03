import re


SUBJECTS = ["Spanish", "English", "Social Studies", "Science"]


def is_valid_name(name):
    return bool(name.strip()) and not any(char.isdigit() for char in name)


def is_valid_section(section):
    pattern = r"^[0-9]{1,2}[A-Z]$"
    return re.match(pattern, section) is not None


def student_exists(students, full_name, section):
    for student in students:
        if (
            student["full_name"].lower() == full_name.lower()
            and student["section"].upper() == section.upper()
        ):
            return True
    return False


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

            if 0 <= grade <= 100:
                return grade

            print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def calculate_average(student):
    total = (
        student["spanish_grade"]
        + student["english_grade"]
        + student["social_studies_grade"]
        + student["science_grade"]
    )
    return total / 4


def add_students(students):
    while True:
        try:
            amount = int(input("How many students do you want to add? "))

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
            "spanish_grade": get_valid_grade("Spanish"),
            "english_grade": get_valid_grade("English"),
            "social_studies_grade": get_valid_grade("Social Studies"),
            "science_grade": get_valid_grade("Science"),
        }

        students.append(student)
        print("Student added successfully.")


def show_students(students):
    if not students:
        print("There are no students registered.")
        return

    print("\n===== Students List =====")

    for student in students:
        average = calculate_average(student)

        print("\n--------------------------")
        print(f"Full name: {student['full_name']}")
        print(f"Section: {student['section']}")
        print(f"Spanish: {student['spanish_grade']}")
        print(f"English: {student['english_grade']}")
        print(f"Social Studies: {student['social_studies_grade']}")
        print(f"Science: {student['science_grade']}")
        print(f"Average: {average:.2f}")


def show_top_three_students(students):
    if not students:
        print("There are no students registered.")
        return

    sorted_students = sorted(
        students,
        key=calculate_average,
        reverse=True
    )

    print("\n===== Top 3 Students =====")

    for index, student in enumerate(sorted_students[:3], start=1):
        print(
            f"{index}. {student['full_name']} - "
            f"Section: {student['section']} - "
            f"Average: {calculate_average(student):.2f}"
        )


def show_general_average(students):
    if not students:
        print("There are no students registered.")
        return

    total_average = 0

    for student in students:
        total_average += calculate_average(student)

    general_average = total_average / len(students)

    print(f"The general average is: {general_average:.2f}")


def delete_student(students):
    if not students:
        print("There are no students registered.")
        return

    full_name = input("Enter the full name of the student to delete: ").strip()
    section = input("Enter the section of the student: ").strip().upper()

    for student in students:
        if (
            student["full_name"].lower() == full_name.lower()
            and student["section"].upper() == section
        ):
            confirmation = input(
                f"Are you sure you want to delete {full_name} from {section}? (yes/no): "
            ).lower()

            if confirmation == "yes":
                students.remove(student)
                print("Student deleted successfully.")
            else:
                print("Deletion cancelled.")

            return

    print("Student not found.")


def show_failed_students(students):
    if not students:
        print("There are no students registered.")
        return

    found_failed_students = False

    print("\n===== Failed Students =====")

    for student in students:
        failed_subjects = []

        if student["spanish_grade"] < 60:
            failed_subjects.append(("Spanish", student["spanish_grade"]))
        if student["english_grade"] < 60:
            failed_subjects.append(("English", student["english_grade"]))
        if student["social_studies_grade"] < 60:
            failed_subjects.append(("Social Studies", student["social_studies_grade"]))
        if student["science_grade"] < 60:
            failed_subjects.append(("Science", student["science_grade"]))

        if failed_subjects:
            found_failed_students = True
            print("\n--------------------------")
            print(f"Full name: {student['full_name']}")
            print(f"Section: {student['section']}")
            print("Failed subjects:")

            for subject, grade in failed_subjects:
                print(f"- {subject}: {grade}")

    if not found_failed_students:
        print("There are no failed students.")