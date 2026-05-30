"""Audit logs API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_audits():
    return []
