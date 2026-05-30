"""Authentication endpoints"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    return {"detail": "Not implemented"}

@router.post("/refresh")
async def refresh():
    return {"detail": "Not implemented"}
