"""AgentPlayground API - Main application entry point."""
from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Original project routers (app/api/)
from app.api.health import router as health_router
from app.api.signals import router as signals_router
from app.api.assets import router as assets_router
from app.api.portfolio import router as portfolio_router
from app.api.backtests import router as backtests_router
from app.api.audits import router as audits_router
from app.api.data_sources import router as data_sources_router
from app.api.events import router as events_router

# Our custom agents router
from app.routers.agents import router as agents_router

from app.config import settings
from app.logging import setup_logging
from app.telemetry import setup_telemetry

APP_VERSION = "0.1.0"
API_PREFIX = "/api/v1"
DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    setup_logging()
    if settings.otel_enabled:
        setup_telemetry()
    yield

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="AgentPlayground API",
        description="Agentic hedge-fund research copilot and market intelligence platform",
        version=APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=DEFAULT_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_v1 = APIRouter(prefix=API_PREFIX)

    # Register routers
    api_v1.include_router(health_router, tags=["health"])
    api_v1.include_router(agents_router, prefix="/agents", tags=["agents"])
    api_v1.include_router(signals_router, prefix="/signals", tags=["signals"])
    api_v1.include_router(assets_router, prefix="/assets", tags=["assets"])
    api_v1.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
    api_v1.include_router(backtests_router, prefix="/backtests", tags=["backtests"])
    api_v1.include_router(audits_router, prefix="/audits", tags=["audits"])
    api_v1.include_router(data_sources_router, prefix="/data", tags=["data"])
    api_v1.include_router(events_router, prefix="/events", tags=["events"])

    app.include_router(api_v1)

    register_compatibility_routes(app)
    register_root_routes(app)
    return app

def register_compatibility_routes(app: FastAPI) -> None:
    """Register minimal backward-compatible routes."""
    app.include_router(health_router, prefix="/health", tags=["health-compat"])

def register_root_routes(app: FastAPI) -> None:
    """Register root-level informational endpoints."""
    @app.get("/", tags=["root"])
    async def root() -> dict[str, str | bool]:
        return {
            "name": "AgentPlayground API",
            "version": APP_VERSION,
            "status": "operational",
            "environment": settings.environment,
            "paper_trading": settings.paper_trading_enabled,
            "live_trading": settings.live_trading_enabled,
        }

    @app.get(f"{API_PREFIX}/version", tags=["health"])
    async def version() -> dict[str, str]:
        return {
            "version": APP_VERSION,
            "api_version": "v1",
        }

app = create_app()