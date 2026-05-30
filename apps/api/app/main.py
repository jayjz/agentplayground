"""
AgentPlayground API - Main application entry point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging import setup_logging
from app.telemetry import setup_telemetry
from app.api import health, signals, events, agents, portfolio, backtests, audits, data_sources, assets, seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    setup_logging()
    if settings.otel_enabled:
        setup_telemetry()
    
    yield
    
    # Shutdown
    pass


app = FastAPI(
    title="AgentPlayground API",
    description="Agentic hedge-fund research copilot and market intelligence platform",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioned API router
api_v1 = APIRouter(prefix="/api/v1")

# Include routers under /api/v1
api_v1.include_router(health.router, tags=["health"])
api_v1.include_router(assets.router, prefix="/assets", tags=["assets"])
api_v1.include_router(signals.router, prefix="/signals", tags=["signals"])
api_v1.include_router(events.router, prefix="/events", tags=["events"])
api_v1.include_router(agents.router, prefix="/agents", tags=["agents"])
api_v1.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_v1.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
api_v1.include_router(audits.router, prefix="/audits", tags=["audits"])
api_v1.include_router(seed.router, prefix="/seed", tags=["seed"])
api_v1.include_router(data_sources.router, prefix="/data", tags=["data"])

app.include_router(api_v1)

# Compatibility aliases (redirect to v1)
app.include_router(health.router, prefix="/health", tags=["health-compat"])


@app.get("/")
async def root():
    return {
        "name": "AgentPlayground API",
        "version": "0.1.0",
        "status": "operational",
        "environment": settings.environment,
        "paper_trading": settings.paper_trading_enabled,
        "live_trading": settings.live_trading_enabled,
    }


@app.get("/api/v1/version")
async def version():
    return {
        "version": "0.1.0",
        "api_version": "v1",
    }
