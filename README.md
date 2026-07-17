# EduControl

Sistema de control académico construido con Python y FastAPI. Permite administrar expedientes estudiantiles, consultar indicadores de rendimiento e importar o exportar información en CSV desde una interfaz web responsiva.

El proyecto conserva la aplicación de consola original y reutiliza sus reglas de validación y cálculo. La interfaz web utiliza persistencia relacional mediante SQLAlchemy y migraciones versionadas con Alembic.

## Características

- Dashboard con matrícula total, promedio general, aprobados y estudiantes en riesgo.
- Distribución de estudiantes por sección.
- Registro, consulta, edición y eliminación de expedientes.
- Búsqueda por nombre, filtro por sección y paginación.
- Calificaciones por materia y promedio individual.
- Reportes de los tres mejores promedios y materias reprobadas.
- Importación y exportación CSV con validación y control de duplicados.
- Datos de demostración idempotentes.
- Mensajes claros, estados vacíos y diseño adaptable a dispositivos móviles.
- API REST con documentación OpenAPI.
- Aplicación de consola original disponible.

## Tecnologías

- Python 3.11+
- FastAPI y Uvicorn
- SQLAlchemy 2
- Alembic
- PostgreSQL con Psycopg 3
- SQLite para desarrollo local y pruebas
- Pydantic 2
- HTML5, CSS y JavaScript
- `unittest` y FastAPI TestClient
- Railway Railpack para un futuro despliegue sin Docker

## Arquitectura

```text
Navegador / cliente API
          │
          ▼
     Rutas FastAPI
          │
          ▼
       Servicios
          │
          ▼
     Repositorios
          │
          ▼
 SQLAlchemy ── PostgreSQL / SQLite
```

- `routes`: contratos HTTP, parámetros y códigos de respuesta.
- `services`: casos de uso, serialización e importación/exportación.
- `repository`: consultas y persistencia.
- `models`: entidades SQLAlchemy y restricciones.
- `schemas`: validación y respuestas Pydantic.
- `actions`: reglas académicas compartidas con la consola.

## Estructura del proyecto

```text
.
├── .github/workflows/       # integración continua
├── docs/screenshots/        # capturas para el portafolio
├── migrations/              # configuración y versiones Alembic
├── src/student_control_system/
│   ├── routes/              # endpoints FastAPI
│   ├── web/                 # interfaz HTML, CSS y JavaScript
│   ├── actions.py           # reglas de negocio compartidas
│   ├── api.py               # aplicación FastAPI
│   ├── config.py            # carga de variables de entorno
│   ├── database.py          # engine y sesiones SQLAlchemy
│   ├── demo_data.py         # datos de demostración
│   ├── models.py            # modelos ORM
│   ├── repository.py        # acceso a datos
│   ├── schemas.py           # esquemas Pydantic
│   └── services.py          # casos de uso
├── tests/                   # pruebas unitarias y de endpoints
├── main.py                  # aplicación de consola
├── alembic.ini
├── pyproject.toml
└── railway.toml             # configuración futura de Railway
```

## Instalación local en Windows PowerShell

### 1. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si la política de PowerShell impide activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar el proyecto

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

### 3. Configurar la base de datos

```powershell
Copy-Item .env.example .env
```

Para PostgreSQL:

```dotenv
DATABASE_URL=postgresql+psycopg://student_app:tu_contrasena@localhost:5432/student_control
```

Para una demostración local con SQLite:

```dotenv
DATABASE_URL=sqlite:///./student_control.db
```

Si `DATABASE_URL` no está definida fuera de Railway, la aplicación usa SQLite local. En Railway la variable es obligatoria para evitar utilizar accidentalmente almacenamiento efímero.

### 4. Ejecutar migraciones

```powershell
alembic upgrade head
```

### 5. Cargar datos de demostración

```powershell
python -m student_control_system.demo_data
```

El comando agrega diez estudiantes distribuidos en varias secciones. Puede repetirse de forma segura: los registros existentes se omiten.

### 6. Iniciar la aplicación

```powershell
uvicorn student_control_system.api:app --reload
```

Servicios disponibles:

- Aplicación web: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Estado del servicio y base de datos: <http://localhost:8000/health>

## Aplicación de consola

```powershell
python main.py
```

La consola mantiene registro, listado, búsqueda, edición, reportes, eliminación e importación/exportación CSV. Su comportamiento histórico no depende de la base de datos web.

## Variables de entorno

| Variable | Entorno | Descripción |
|---|---|---|
| `DATABASE_URL` | Local | Opcional; si falta, usa `sqlite:///./student_control.db`. |
| `DATABASE_URL` | Railway | Obligatoria; debe referenciar el servicio PostgreSQL. |
| `PORT` | Railway | La proporciona Railway y es utilizada por `railway.toml`. |

`.env`, archivos SQLite y entornos virtuales están ignorados por Git. Nunca agregues credenciales reales al repositorio.

## Pruebas

```powershell
python -m unittest discover -v
```

Las pruebas cubren:

- validaciones y cálculos académicos;
- CRUD y filtros;
- dashboard y reportes;
- importación/exportación CSV;
- repositorios y restricciones;
- carga idempotente de datos;
- normalización de la URL PostgreSQL de Railway;
- health check con conexión a la base de datos.

## Despliegue futuro en Railway

El repositorio incluye `railway.toml` y utiliza Railpack; no requiere Docker.

1. Crea un proyecto en Railway desde el repositorio de GitHub.
2. Agrega un servicio PostgreSQL.
3. Define `DATABASE_URL` en el servicio web usando la referencia del PostgreSQL.
4. Railway ejecutará `alembic upgrade head` antes de publicar.
5. El proceso inicia con:

   ```text
   uvicorn student_control_system.api:app --host 0.0.0.0 --port $PORT
   ```

6. El health check se realiza contra `/health`.
7. Genera un dominio público y verifica `/`, `/docs` y `/health`.

No cargues datos demo automáticamente en producción. Si los necesitas para una presentación, ejecuta el comando manualmente una sola vez desde un entorno controlado.

## Capturas

Ubicación: [`docs/screenshots`](docs/screenshots)

Marcadores pendientes:

- `dashboard.png`
- `students.png`
- `student-form.png`
- `reports.png`
- `swagger.png`

```md
![Dashboard](docs/screenshots/dashboard.png)
![Gestión de estudiantes](docs/screenshots/students.png)
```

## Decisiones y limitaciones

- PostgreSQL es la base de datos objetivo de producción.
- SQLite se conserva para desarrollo y pruebas.
- No se implementó autenticación ni autorización; quedan fuera del alcance actual.
- La consola usa memoria/CSV para preservar compatibilidad.
- El despliegue debe validarse primero en un entorno de Railway separado de producción.
