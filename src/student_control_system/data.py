import csv
import os

from .actions import (
    STUDENT_FIELDS,
    SUBJECTS,
    is_valid_grade,
    is_valid_name,
    is_valid_section,
)


FILE_NAME = "students.csv"


def export_to_csv(students):
    if not students:
        print("There are no students to export.")
        return

    try:
        with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=STUDENT_FIELDS)
            writer.writeheader()
            writer.writerows(students)

        print(f"Data exported successfully to {FILE_NAME}.")
    except Exception as error:
        print(f"Export failed: {error}")


def validate_csv_headers(fieldnames):
    if fieldnames is None:
        raise ValueError("The CSV file is empty.")

    missing_fields = [field for field in STUDENT_FIELDS if field not in fieldnames]

    if missing_fields:
        raise ValueError(f"Missing required columns: {', '.join(missing_fields)}")


def build_student_from_row(row, row_number):
    full_name = row["full_name"].strip()
    section = row["section"].strip().upper()

    if not is_valid_name(full_name):
        raise ValueError(f"Invalid full name in row {row_number}.")

    if not is_valid_section(section):
        raise ValueError(f"Invalid section in row {row_number}.")

    student = {
        "full_name": full_name,
        "section": section,
    }

    for subject, field_name in SUBJECTS:
        try:
            grade = float(row[field_name])
        except ValueError as error:
            raise ValueError(f"Invalid {subject} grade in row {row_number}.") from error

        if not is_valid_grade(grade):
            raise ValueError(
                f"{subject} grade in row {row_number} must be between 0 and 100."
            )

        student[field_name] = grade

    return student


def import_from_csv():
    if not os.path.exists(FILE_NAME):
        print("There is no previously exported CSV file.")
        return None

    students = []

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            validate_csv_headers(reader.fieldnames)

            for row_number, row in enumerate(reader, start=2):
                students.append(build_student_from_row(row, row_number))

        print(f"Data imported successfully from {FILE_NAME}.")
        return students

    except Exception as error:
        print(f"Import failed: {error}")
        return None
