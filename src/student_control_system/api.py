import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .database import get_session
from .routes.students import router as students_router


logger = logging.getLogger(__name__)
WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(
    title="Student Control System API",
    version="3.0.0",
    description="API REST para expedientes, calificaciones e indicadores académicos.",
)
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


app.include_router(students_router)


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, error: Exception):
    logger.exception("Unhandled error while processing %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocurrió un error inesperado. Intenta nuevamente."},
    )


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def web_app():
    return FileResponse(WEB_DIR / "index.html")
