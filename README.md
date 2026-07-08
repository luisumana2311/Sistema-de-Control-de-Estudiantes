# Student Control System

A Python console application for managing student records, grades, academic averages, CSV import/export, and failed-subject reports.

This project started as a fundamentals exercise and is being improved as a professional junior/full-stack portfolio project. The current version keeps the original console experience while adding cleaner structure, validations, error handling, tests, and project documentation.

## Features

- Register students with full name and section.
- Validate names, sections, and grades.
- Show all registered students with subject grades and average.
- Show the top 3 students by average.
- Calculate the general class average.
- Delete students with confirmation.
- Show students with failed subjects.
- Export student records to CSV.
- Import student records from CSV.

## Technologies

- Python 3
- Standard library only:
  - `csv`
  - `os`
  - `re`
  - `unittest`

## Project Structure

```text
student_control_system/
├── actions.py      # Business rules, validation, and student operations
├── data.py         # CSV persistence
├── main.py         # Application entry point
├── menu.py         # Console menu and user flow
├── tests/          # Unit tests
├── .gitignore      # Ignored generated/local files
└── README.md       # Project documentation
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd student_control_system
```

2. Optional: create and activate a virtual environment.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Run the application:

```bash
python main.py
```

## Running Tests

```bash
python -m unittest discover
```

## CSV Format

The CSV file uses the following columns:

```text
full_name,section,spanish_grade,english_grade,social_studies_grade,science_grade
```

Grades must be numeric values between `0` and `100`.

## Screenshots

Screenshots can be added here as the UI evolves.

Suggested screenshots:

- Main menu.
- Student registration flow.
- Student list.
- Top 3 students report.
- Failed students report.

```md
![Main menu](docs/screenshots/main-menu.png)
![Student list](docs/screenshots/student-list.png)
```

## Roadmap

### P0 - Professional Foundation

- [x] Add professional README.
- [x] Add `.gitignore`.
- [x] Remove generated Python cache files from version control.
- [x] Improve validation and CSV error handling.
- [x] Add basic unit tests.

### P1 - Functional Improvements

- [ ] Add edit-student functionality.
- [ ] Add search and filters by section or academic status.
- [ ] Add automatic loading or save confirmation.
- [ ] Improve console formatting for reports.
- [ ] Add summary reports by section.

### P2 - Portfolio Differentiators

- [ ] Reorganize into a `src/` package architecture.
- [ ] Add CI with GitHub Actions.
- [ ] Add code formatting and linting.
- [ ] Add a web UI or REST API while reusing the domain logic.
- [ ] Add real screenshots and a short architecture section.

## GitHub Best Practices

- Keep generated files out of version control.
- Use small, descriptive commits.
- Document setup and test commands.
- Keep business logic separate from input/output code where possible.
- Add tests for validation and data persistence behavior.
