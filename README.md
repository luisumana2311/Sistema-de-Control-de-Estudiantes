# EduControl — Sistema de Control de Estudiantes

Aplicación académica para administrar estudiantes, calificaciones y seguimiento de rendimiento. Mantiene el flujo original de consola y añade una aplicación web responsiva con API REST documentada.

## Funcionalidades

- Dashboard: total, promedio general, aprobados, riesgo académico y distribución por sección.
- Registro, consulta, búsqueda, filtro, edición y eliminación con confirmación.
- Calificaciones de Español, Inglés, Estudios Sociales y Ciencias; promedio individual.
- Reportes de los tres mejores estudiantes y estudiantes con materias reprobadas.
- Importación y exportación CSV.
- Validaciones de nombres, secciones (`10A`, `11B`) y notas entre 0 y 100.
- Mensajes de éxito/error sin exponer trazas internas.
- Datos de demostración idempotentes.
- Consola original disponible mediante `python main.py`.
- Swagger en `/docs` y ReDoc en `/redoc`.

## Arquitectura

```text
src/student_control_system/
├── actions.py          # reglas compartidas con la consola
├── api.py              # composición de FastAPI y manejo global de errores
├── config.py           # carga segura de variables desde .env
├── database.py         # engine, sesiones y Base de SQLAlchemy
├── models.py           # modelos ORM Student y Grade
├── schemas.py          # contratos Pydantic
├── repository.py       # acceso a datos y consultas
├── services.py         # casos de uso, CSV y serialización
├── routes/students.py  # endpoints HTTP
├── demo_data.py        # carga idempotente de datos demo
├── menu.py / data.py   # flujo original de consola
└── web/                # HTML, CSS y JavaScript responsivos
```

El flujo es `web/API → rutas → servicios → repositorios → SQLAlchemy → base de datos`. Las validaciones y cálculos académicos existentes en `actions.py` se reutilizan tanto en consola como en web.

## Tecnologías implementadas

- Python 3.11+
- FastAPI y Uvicorn
- SQLAlchemy 2
- Alembic
- PostgreSQL con `psycopg` como base principal
- SQLite como alternativa explícita para desarrollo local
- Pydantic 2
- HTML5, CSS y JavaScript sin framework de frontend
- `unittest`, FastAPI TestClient y SQLite en memoria para pruebas

## Configuración local — Windows PowerShell

Desde la raíz del repositorio:

### 1. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecuta una vez en esa terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

### 3. Configurar variables de entorno

```powershell
Copy-Item .env.example .env
```

Edita `.env` con una de estas opciones:

```dotenv
# PostgreSQL recomendado
DATABASE_URL=postgresql+psycopg://student_app:tu_contrasena@localhost:5432/student_control
```

```dotenv
# SQLite solo para una demo local rápida
DATABASE_URL=sqlite:///./student_control.db
```

No guardes credenciales reales en Git; `.env` está ignorado.

Para crear PostgreSQL desde `psql` con un usuario administrador:

```sql
CREATE USER student_app WITH PASSWORD 'elige_una_contrasena_segura';
CREATE DATABASE student_control OWNER student_app;
```

### 4. Ejecutar migraciones

```powershell
alembic upgrade head
```

### 5. Cargar datos de demostración (opcional)

```powershell
python -m student_control_system.demo_data
```

Se agregan diez estudiantes en cinco secciones. El comando es seguro para repetirse: los registros existentes se omiten.

### 6. Iniciar la aplicación web

```powershell
uvicorn student_control_system.api:app --reload
```

Abre:

- Aplicación: <http://localhost:8000>
- Swagger: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Salud: <http://localhost:8000/health>

### 7. Ejecutar pruebas

```powershell
python -m unittest discover -v
```

## Aplicación de consola

El flujo original no fue eliminado ni conectado obligatoriamente a la base web:

```powershell
python main.py
```

Incluye registro, listado, búsqueda, edición, top 3, promedio general, CSV, eliminación y reporte de reprobados.

## Formato CSV

```csv
full_name,section,spanish_grade,english_grade,social_studies_grade,science_grade
Ana Rivera,11A,90,85,88,92
```

Los duplicados por nombre normalizado y sección se omiten al importar. Las filas inválidas se reportan sin detener las filas válidas.

## Variables de entorno

| Variable | Requerida | Descripción |
|---|---:|---|
| `DATABASE_URL` | Sí | URL de SQLAlchemy para PostgreSQL o SQLite local. |

Si no se define, se usa una URL PostgreSQL local de desarrollo; se recomienda siempre crear `.env`.

## Capturas

Guarda las capturas de la demostración en [`docs/screenshots`](docs/screenshots). Capturas sugeridas:

- Dashboard con datos demo.
- Tabla con búsqueda y filtro.
- Formulario de edición.
- Reportes de top 3 y materias reprobadas.
- Swagger mostrando los endpoints.

## Estado y limitaciones

- PostgreSQL, SQLAlchemy, Alembic y FastAPI están implementados en código, no solo documentados.
- SQLite está pensado únicamente para desarrollo y pruebas.
- No hay autenticación ni roles; quedan fuera del alcance actual.
- La consola conserva almacenamiento en memoria/CSV para no romper su comportamiento histórico; la web usa la base de datos.
