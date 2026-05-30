"""
Signals API endpoints - DB-backed implementation
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_session
from app.db.models.factor_signal import FactorSignal

router = APIRouter()


@router.get("/")
async def list_signals(
    ticker: Optional[str] = None,
    signal_type: Optional[str] = None,
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_session),
):
    """List research signals from database"""
    query = select(FactorSignal).limit(limit)
    
    result = await db.execute(query)
    signals = result.scalars().all()
    
    items = [
        {
            "id": str(signal.id),
            "asset_id": str(signal.asset_id),
            "signal_date": signal.signal_date.isoformat() if signal.signal_date else None,
            "signal_type": signal.signal_type,
            "raw_value": float(signal.raw_value) if signal.raw_value else None,
            "normalized_value": float(signal.normalized_value) if signal.normalized_value else None,
            "score": float(signal.score),
            "confidence": float(signal.confidence),
            "horizon": signal.horizon,
            "rationale": signal.rationale,
            "created_at": signal.created_at.isoformat() if signal.created_at else None,
        }
        for signal in signals
    ]
    
    return {
        "items": items,
        "count": len(items)
    }


@router.get("/{signal_id}")
async def get_signal(signal_id: str, db: AsyncSession = Depends(get_session)):
    """Get signal by ID"""
    result = await db.execute(
        select(FactorSignal).where(FactorSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    
    if not signal:
        return {"detail": "Signal not found"}, 404
    
    return {
        "item": {
            "id": str(signal.id),
            "asset_id": str(signal.asset_id),
            "signal_type": signal.signal_type,
            "score": float(signal.score),
            "confidence": float(signal.confidence),
        }
    }
