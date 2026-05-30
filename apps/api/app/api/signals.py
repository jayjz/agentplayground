"""
Signals API endpoints - P0 implementation with memory store
"""
from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import datetime
from app.db.memory_store import store

router = APIRouter()


@router.get("/")
async def list_signals(
    ticker: Optional[str] = None,
    signal_type: Optional[str] = None,
    limit: int = Query(100, le=1000),
):
    """List research signals"""
    signals = store.get_signals(limit)
    
    # Apply filters
    if ticker:
        signals = [s for s in signals if s.get("ticker") == ticker]
    if signal_type:
        signals = [s for s in signals if s.get("signal_type") == signal_type]
    
    return {
        "items": signals,
        "count": len(signals)
    }


@router.get("/{signal_id}")
async def get_signal(signal_id: str):
    """Get signal by ID"""
    signals = store.get_signals(1000)
    for signal in signals:
        if signal.get("id") == signal_id:
            return {"item": signal}
    
    return {"detail": "Signal not found"}, 404
