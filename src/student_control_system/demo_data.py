"""Carga idempotente de datos de demostración."""

from sqlalchemy.exc import IntegrityError

from .database import SessionFactory
from .repository import StudentRepository


DEMO_STUDENTS = [
    ("María Solano", "10A", 94, 91, 89, 96),
    ("Daniel Jiménez", "10A", 78, 82, 75, 80),
    ("Sofía Vargas", "10B", 99, 96, 95, 98),
    ("Carlos Mora", "10B", 58, 62, 55, 57),
    ("Valentina Rojas", "11A", 88, 93, 90, 91),
    ("José Hernández", "11A", 70, 54, 68, 73),
    ("Lucía Castro", "11B", 85, 87, 84, 89),
    ("Andrés Quesada", "11B", 45, 52, 59, 48),
    ("Camila Ramírez", "12A", 92, 94, 97, 90),
    ("Mateo Chaves", "12A", 65, 71, 58, 69),
]


def seed_demo_data(session=None):
    owns_session = session is None
    session = session or SessionFactory()
    repository = StudentRepository(session)
    created = 0
    skipped = 0
    try:
        for name, section, spanish, english, social, science in DEMO_STUDENTS:
            payload = {
                "full_name": name,
                "section": section,
                "spanish_grade": spanish,
                "english_grade": english,
                "social_studies_grade": social,
                "science_grade": science,
            }
            try:
                repository.create(payload)
                created += 1
            except IntegrityError:
                session.rollback()
                skipped += 1
        return created, skipped
    finally:
        if owns_session:
            session.close()


def main():
    created, skipped = seed_demo_data()
    print(f"Datos demo listos: {created} creados, {skipped} ya existentes.")


if __name__ == "__main__":
    main()
