from actions import (
    add_students,
    edit_student,
    get_confirmation,
    search_student,
    show_students,
    show_top_three_students,
    show_general_average,
    delete_student,
    show_failed_students,
)
from data import export_to_csv, import_from_csv


MENU_OPTIONS = {
    "1": "Add students",
    "2": "Show all students",
    "3": "Search student by name",
    "4": "Edit student",
    "5": "Show top 3 students",
    "6": "Show general average",
    "7": "Export data to CSV",
    "8": "Import data from CSV",
    "9": "Delete student",
    "10": "Show failed students",
    "11": "Exit",
}


def get_menu_option():
    while True:
        option = input("Choose an option: ").strip()

        if option in MENU_OPTIONS:
            return option

        valid_options = ", ".join(MENU_OPTIONS.keys())
        print(f"Invalid option. Choose one of: {valid_options}.")


def show_menu(students):
    while True:
        print("\n===== Student Control System =====")
        for option, label in MENU_OPTIONS.items():
            print(f"{option}. {label}")

        option = get_menu_option()

        if option == "1":
            add_students(students)

        elif option == "2":
            show_students(students)

        elif option == "3":
            search_student(students)

        elif option == "4":
            edit_student(students)

        elif option == "5":
            show_top_three_students(students)

        elif option == "6":
            show_general_average(students)

        elif option == "7":
            export_to_csv(students)

        elif option == "8":
            if get_confirmation(
                "Importing a CSV will replace the current student list. Do you want to continue?"
            ):
                imported_students = import_from_csv()

                if imported_students is not None:
                    students.clear()
                    students.extend(imported_students)
                    print("Students imported successfully.")
            else:
                print("Import cancelled.")

        elif option == "9":
            delete_student(students)

        elif option == "10":
            show_failed_students(students)

        elif option == "11":
            print("Exiting system...")
            break
