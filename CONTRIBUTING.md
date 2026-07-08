# Contributing

Thanks for your interest in improving Student Control System.

This is a portfolio-focused Python console application, so contributions should keep the project simple, readable, and beginner-friendly.

## Local Setup

1. Clone the repository.
2. Optional: create a virtual environment.
3. Run the app:

```bash
python main.py
```

4. Run tests:

```bash
python -m unittest discover
```

## Guidelines

- Keep the main technology as Python and the standard library unless there is a clear reason to add a dependency.
- Keep console behavior compatible with `python main.py`.
- Add or update tests when changing validation, calculations, reports, imports, exports, or menu behavior.
- Prefer small, descriptive commits.
- Do not commit generated files such as `__pycache__`, local CSV exports, or virtual environments.

## Pull Request Checklist

- [ ] The application still runs with `python main.py`.
- [ ] Tests pass with `python -m unittest discover`.
- [ ] README or docs are updated when user-facing behavior changes.
- [ ] The change is focused and does not remove existing functionality.
