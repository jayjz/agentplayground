"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.dependencies import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "agentplayground-api",
        "version": "0.1.0",
    }


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Readiness check with database connectivity"""
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "ready" if db_status == "connected" else "not_ready",
        "database": db_status,
        "timestamp": "2026-05-30T18:12:00Z",  # TODO: Use actual timestamp
    }


@router.get("/live")
async def liveness_check():
    """Liveness probe"""
    return {"status": "alive"}
