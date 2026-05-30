"""Signals API endpoints - DB-backed implementation."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.asset import Asset
from app.db.models.factor_signal import FactorSignal
from app.db.session import get_session

router = APIRouter()


def serialize_signal(signal: FactorSignal) -> dict[str, Any]:
    """Serialize a FactorSignal ORM object into a JSON-safe dictionary."""
    return {
        "id": str(signal.id),
        "asset_id": str(signal.asset_id),
        "signal_date": signal.signal_date.isoformat() if signal.signal_date else None,
        "signal_type": signal.signal_type,
        "raw_value": float(signal.raw_value) if signal.raw_value is not None else None,
        "normalized_value": (
            float(signal.normalized_value)
            if signal.normalized_value is not None
            else None
        ),
        "score": float(signal.score) if signal.score is not None else None,
        "confidence": float(signal.confidence) if signal.confidence is not None else None,
        "horizon": signal.horizon,
        "rationale": signal.rationale,
        "created_at": signal.created_at.isoformat() if signal.created_at else None,
        "updated_at": signal.updated_at.isoformat() if getattr(signal, "updated_at", None) else None,
    }


@router.get("/")
async def list_signals(
    db: AsyncSession = Depends(get_session),
    ticker: str | None = Query(default=None, description="Filter by asset symbol"),
    signal_type: str | None = Query(default=None, description="Filter by signal type"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of signals to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
) -> dict[str, Any]:
    """List factor signals from the database with optional filtering."""
    stmt: Select[tuple[FactorSignal]] = select(FactorSignal)

    if ticker:
        stmt = stmt.join(Asset, FactorSignal.asset_id == Asset.id).where(
            Asset.symbol == ticker.upper()
        )

    if signal_type:
        stmt = stmt.where(FactorSignal.signal_type == signal_type)

    stmt = (
        stmt.order_by(
            FactorSignal.signal_date.desc().nullslast(),
            FactorSignal.created_at.desc().nullslast(),
        )
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(stmt)
    signals = result.scalars().all()

    items = [serialize_signal(signal) for signal in signals]

    return {
        "items": items,
        "count": len(items),
    }


@router.get("/{signal_ref}")
async def get_signal(
    signal_ref: str,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Get a signal by UUID."""
    try:
        signal_uuid = UUID(signal_ref)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid signal ID: {signal_ref}",
        ) from exc

    result = await db.execute(
        select(FactorSignal).where(FactorSignal.id == signal_uuid)
    )
    signal = result.scalar_one_or_none()

    if signal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Signal not found: {signal_ref}",
        )

    return {
        "item": serialize_signal(signal),
    }
