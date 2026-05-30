"""Assets API - DB-backed implementation"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.db.models.asset import Asset

router = APIRouter()

@router.get("/")
async def list_assets(db: AsyncSession = Depends(get_session)):
    """List assets from database"""
    result = await db.execute(select(Asset))
    assets = result.scalars().all()
    
    items = [
        {
            "id": str(asset.id),
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type": asset.asset_type,
            "sector": asset.sector,
            "industry": asset.industry,
            "exchange": asset.exchange,
            "is_active": asset.is_active,
            "created_at": asset.created_at.isoformat() if asset.created_at else None,
        }
        for asset in assets
    ]
    
    return {
        "items": items,
        "count": len(items)
    }

@router.get("/{asset_id}")
async def get_asset(asset_id: str, db: AsyncSession = Depends(get_session)):
    """Get asset by ID"""
    result = await db.execute(
        select(Asset).where(
            (Asset.id == asset_id) | (Asset.symbol == asset_id.upper())
        )
    )
    asset = result.scalar_one_or_none()
    
    if not asset:
        return {"detail": "Asset not found"}, 404
    
    return {
        "item": {
            "id": str(asset.id),
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type": asset.asset_type,
            "sector": asset.sector,
            "industry": asset.industry,
            "exchange": asset.exchange,
            "is_active": asset.is_active,
        }
    }
