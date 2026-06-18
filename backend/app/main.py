"""FastAPI application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import (
    activities_router,
    contacts_router,
    deals_router,
    pipelines_router,
    stats_router,
    users_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (dev convenience; use Alembic in production)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @app.get("/health", tags=["system"])
    async def health_check():
        return {"status": "ok", "version": settings.app_version}

    # Register routers
    app.include_router(contacts_router)
    app.include_router(deals_router)
    app.include_router(activities_router)
    app.include_router(pipelines_router)
    app.include_router(users_router)
    app.include_router(stats_router)

    return app


app = create_app()
