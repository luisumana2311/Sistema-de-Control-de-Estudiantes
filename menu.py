from actions import (
    add_students,
    show_students,
    show_top_three_students,
    show_general_average,
    delete_student,
    show_failed_students,
)
from data import export_to_csv, import_from_csv


def show_menu(students):
    while True:
        print("\n===== Student Control System =====")
        print("1. Add students")
        print("2. Show all students")
        print("3. Show top 3 students")
        print("4. Show general average")
        print("5. Export data to CSV")
        print("6. Import data from CSV")
        print("7. Delete student")
        print("8. Show failed students")
        print("9. Exit")

        option = input("Choose an option: ")

        if option == "1":
            add_students(students)

        elif option == "2":
            show_students(students)

        elif option == "3":
            show_top_three_students(students)

        elif option == "4":
            show_general_average(students)

        elif option == "5":
            export_to_csv(students)

        elif option == "6":
            confirmation = input(
                "Importing a CSV will replace the current student list. Do you want to continue? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":
                imported_students = import_from_csv()

                if imported_students is not None:
                    students.clear()
                    students.extend(imported_students)
                    print("Students imported successfully.")
            else:
                print("Import cancelled.")

        elif option == "7":
            delete_student(students)

        elif option == "8":
            show_failed_students(students)

        elif option == "9":
            print("Exiting system...")
            break

        else:
            print("Invalid option. Please try again.")