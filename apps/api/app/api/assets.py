"""Assets API - P0 implementation"""
from fastapi import APIRouter
from app.db.memory_store import store

router = APIRouter()

@router.get("/")
async def list_assets():
    """List assets"""
    assets = store.get_assets()
    return {
        "items": assets,
        "count": len(assets)
    }

@router.get("/{asset_id}")
async def get_asset(asset_id: str):
    """Get asset by ID"""
    assets = store.get_assets()
    for asset in assets:
        if asset.get("id") == asset_id or asset.get("symbol") == asset_id:
            return {"item": asset}
    return {"detail": "Asset not found"}, 404
