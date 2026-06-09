import csv
import os


FILE_NAME = "students.csv"


def export_to_csv(students):
    if not students:
        print("There are no students to export.")
        return

    try:
        with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = [
                "full_name",
                "section",
                "spanish_grade",
                "english_grade",
                "social_studies_grade",
                "science_grade",
            ]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)

        print("Data exported successfully.")
    except Exception as error:
        print(f"An error occurred while exporting data: {error}")


def import_from_csv():
    if not os.path.exists(FILE_NAME):
        print("There is no previously exported CSV file.")
        return None

    students = []

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student = {
                    "full_name": row["full_name"],
                    "section": row["section"],
                    "spanish_grade": float(row["spanish_grade"]),
                    "english_grade": float(row["english_grade"]),
                    "social_studies_grade": float(row["social_studies_grade"]),
                    "science_grade": float(row["science_grade"]),
                }

                students.append(student)

        print("Data imported successfully.")
        return students

    except Exception as error:
        print(f"An error occurred while importing data: {error}")
        return None