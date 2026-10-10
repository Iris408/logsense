"""LogSense API and bundled read-only monitoring dashboard."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models.log_model import LogEntry  # noqa: F401 - register table metadata
from app.routes.log_routes import router as log_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LogSense API",
    description="Log importing, analysis, and a read-only dashboard",
    version="1.0.0",
)
app.include_router(log_router)

DASHBOARD_DIR = Path(__file__).resolve().parent / "dashboard"
app.mount(
    "/dashboard/assets",
    StaticFiles(directory=str(DASHBOARD_DIR)),
    name="dashboard-assets",
)


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(DASHBOARD_DIR / "index.html")


@app.get("/")
def home():
    return {"message": "Welcome to the LogSense API!"}
