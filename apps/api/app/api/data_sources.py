"""Data sources API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_data_sources():
    return [
        {"id": "alpha-vantage", "name": "Alpha Vantage", "type": "market-data"},
        {"id": "fred", "name": "FRED", "type": "macro"},
        {"id": "sec-edgar", "name": "SEC EDGAR", "type": "filings"},
    ]
