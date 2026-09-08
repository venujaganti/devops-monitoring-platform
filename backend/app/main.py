from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.alerts import router as alerts_router
from app.api.applications import router as applications_router
from app.api.auth import router as auth_router
from app.api.incidents import router as incidents_router
from app.api.logs import router as logs_router
from app.api.metrics import router as metrics_router
from app.api.servers import router as servers_router
from app.core.config import settings
from app.database.connection import SessionLocal
from app.database import init_db
from app.database.seed import seed_admin
from app.services.health_service import check_database_health


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_admin()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "DevOps Monitoring and "
        "Incident Management Platform"
    ),
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(servers_router)
app.include_router(metrics_router)
app.include_router(alerts_router)
app.include_router(incidents_router)
app.include_router(applications_router)
app.include_router(logs_router)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health():
    db = SessionLocal()

    try:
        database_ok = check_database_health(db)
    finally:
        db.close()

    return {
        "status": "healthy"
        if database_ok
        else "degraded",
        "database": "connected"
        if database_ok
        else "unavailable",
    }