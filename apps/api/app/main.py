"""
AgentPlayground API - Main application entry point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging import setup_logging
from app.telemetry import setup_telemetry
from app.api import health, signals, events, agents, portfolio, backtests, audits, data_sources


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

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(backtests.router, prefix="/api/backtests", tags=["backtests"])
app.include_router(audits.router, prefix="/api/audits", tags=["audits"])
app.include_router(data_sources.router, prefix="/api/data", tags=["data"])


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
