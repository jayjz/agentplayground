"""Assets API - DB-backed implementation."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.asset import Asset
from app.db.session import get_session

router = APIRouter()


def serialize_asset(asset: Asset) -> dict[str, Any]:
    """Serialize an Asset ORM object into a JSON-safe dictionary."""
    return {
        "id": str(asset.id),
        "symbol": asset.symbol,
        "name": asset.name,
        "asset_type": asset.asset_type,
        "sector": asset.sector,
        "industry": asset.industry,
        "exchange": asset.exchange,
        "is_active": asset.is_active,
        "created_at": asset.created_at.isoformat() if asset.created_at else None,
        "updated_at": asset.updated_at.isoformat() if getattr(asset, "updated_at", None) else None,
    }


@router.get("/")
async def list_assets(
    db: AsyncSession = Depends(get_session),
    is_active: bool | None = Query(default=None, description="Filter by active status"),
    symbol: str | None = Query(default=None, description="Filter by exact symbol"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of assets to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
) -> dict[str, Any]:
    """List assets from the database with optional filtering and deterministic ordering."""
    stmt: Select[tuple[Asset]] = select(Asset)

    if is_active is not None:
        stmt = stmt.where(Asset.is_active == is_active)

    if symbol:
        stmt = stmt.where(Asset.symbol == symbol.upper())

    stmt = stmt.order_by(Asset.symbol.asc()).offset(offset).limit(limit)

    result = await db.execute(stmt)
    assets = result.scalars().all()

    items = [serialize_asset(asset) for asset in assets]

    return {
        "items": items,
        "count": len(items),
    }


@router.get("/{asset_ref}")
async def get_asset(
    asset_ref: str,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """
    Get an asset by UUID or symbol.

    Lookup order:
    1. UUID match if asset_ref parses as UUID
    2. Symbol match using uppercase normalization
    """
    asset: Asset | None = None

    try:
        asset_uuid = UUID(asset_ref)
        result = await db.execute(select(Asset).where(Asset.id == asset_uuid))
        asset = result.scalar_one_or_none()
    except ValueError:
        asset = None

    if asset is None:
        result = await db.execute(
            select(Asset).where(Asset.symbol == asset_ref.upper())
        )
        asset = result.scalar_one_or_none()

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset not found for reference: {asset_ref}",
        )

    return {
        "item": serialize_asset(asset),
    }
