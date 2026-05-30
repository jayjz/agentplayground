"""Agents API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_agents():
    return [
        {"id": "signal-research", "name": "Signal Research Agent", "status": "active"},
        {"id": "event-interpretation", "name": "Event Interpretation Agent", "status": "active"},
        {"id": "regime", "name": "Regime Agent", "status": "active"},
        {"id": "relative-value", "name": "Relative Value Agent", "status": "active"},
        {"id": "risk-narrative", "name": "Risk Narrative Agent", "status": "active"},
    ]
