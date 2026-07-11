# Student Control System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-unittest-green)
![Status](https://img.shields.io/badge/status-portfolio%20ready-brightgreen)

A Python console application for managing student records, grades, academic averages, CSV import/export, search, editing, and academic reports.

This project started as a fundamentals exercise and is being improved as a professional junior/full-stack portfolio project. The current version keeps the original console experience while adding cleaner structure, validations, error handling, tests, and project documentation.

## Features

- Register students with full name and section.
- Validate names, sections, grades, menu options, and confirmations.
- Search students by full or partial name.
- Edit an existing student's name, section, and grades.
- Show all registered students with subject grades and average.
- Show the top 3 students by average.
- Calculate the general class average.
- Delete students with confirmation.
- Show students with failed subjects.
- Export student records to CSV.
- Import student records from CSV.
- Display reports in aligned console tables.

## Technologies

- Python 3
- Python standard-library modules:
  - `csv`
  - `os`
  - `re`
  - `unittest`
  - `unittest.mock`
- PostgreSQL as the production database
- SQLAlchemy 2 for ORM and repository-based persistence
- Alembic for versioned database migrations
- FastAPI with automatic OpenAPI documentation

## Project Structure

```text
student_control_system/
+-- .github/workflows/       # GitHub Actions CI
+-- docs/                    # Portfolio documentation and screenshots
+-- src/
|   +-- student_control_system/
|       +-- actions.py        # Business rules, validation, reports, and operations
|       +-- data.py           # CSV persistence
|       +-- menu.py           # Console menu and user flow
|       +-- __init__.py       # Package marker
+-- tests/                    # Unit tests
+-- main.py                   # Console entry point
+-- CHANGELOG.md              # Project history
+-- CONTRIBUTING.md           # Contribution guidelines
+-- README.md                 # Project documentation
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

### Database foundation

Copy `.env.example` to `.env`, configure a PostgreSQL connection through
`DATABASE_URL`, install the project dependencies, and apply migrations:

```bash
python -m pip install -e .
alembic upgrade head
```

The console workflow remains available while the PostgreSQL repository provides
the persistence foundation for the REST API. SQLite is used only by
isolated repository tests, not as the target production database.

### REST API

Start the API after configuring PostgreSQL and applying the migrations:

```bash
uvicorn student_control_system.api:app --reload
```

The service exposes its health check at `/health`, student CRUD under
`/api/v1/students`, interactive Swagger documentation at `/docs`, and alternative
ReDoc documentation at `/redoc`. Student listings support search, section filters,
and pagination.

## Main Menu

```text
1. Add students
2. Show all students
3. Search student by name
4. Edit student
5. Show top 3 students
6. Show general average
7. Export data to CSV
8. Import data from CSV
9. Delete student
10. Show failed students
11. Exit
```

## Running Tests

```bash
python -m unittest discover
```

Tests also run automatically through GitHub Actions on pushes and pull requests.

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
- Search results.
- Edit student flow.
- Student list.
- Top 3 students report.
- Failed students report.

```md
![Main menu](docs/screenshots/main-menu.png)
![Student list](docs/screenshots/student-list.png)
![Search results](docs/screenshots/search-results.png)
```

More screenshot guidance is available in [docs/README.md](docs/README.md).

## Roadmap

### P0 - Professional Foundation

- [x] Add professional README.
- [x] Add `.gitignore`.
- [x] Remove generated Python cache files from version control.
- [x] Improve validation and CSV error handling.
- [x] Add basic unit tests.

### P1 - Functional Improvements

- [x] Add edit-student functionality.
- [x] Add search by student name.
- [x] Improve console formatting for reports.
- [x] Add clearer menu validation.
- [ ] Add automatic loading or save confirmation.
- [ ] Add filters by section or academic status.
- [ ] Add summary reports by section.

### P2 - Portfolio Differentiators

- [x] Reorganize into a `src/` package architecture.
- [x] Add CI with GitHub Actions.
- [x] Add documentation folder for screenshots.
- [x] Add CHANGELOG and CONTRIBUTING files.
- [ ] Add code formatting and linting.
- [ ] Add a web UI or REST API while reusing the domain logic.
- [ ] Add real screenshots and a short architecture section.

## GitHub Best Practices

- Keep generated files out of version control.
- Use small, descriptive commits.
- Document setup and test commands.
- Keep business logic separate from input/output code where possible.
- Add tests for validation and data persistence behavior.
