"""Portfolio API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_portfolio():
    return {"detail": "Not implemented"}

@router.get("/positions")
async def get_positions():
    return []
