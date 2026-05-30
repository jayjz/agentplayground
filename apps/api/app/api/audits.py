"""Audit logs API - P0 implementation"""
from fastapi import APIRouter, Query
from app.db.memory_store import store

router = APIRouter()

@router.get("/")
async def list_audits(limit: int = Query(100, le=1000)):
    """List audit logs"""
    audits = store.get_audits(limit)
    return {
        "items": audits,
        "count": len(audits)
    }
