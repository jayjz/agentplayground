"""Audit logs API - DB-backed implementation"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.db.models.audit_log import AuditLog

router = APIRouter()

@router.get("/")
async def list_audits(
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_session)
):
    """List audit logs from database"""
    result = await db.execute(
        select(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
    )
    audits = result.scalars().all()
    
    items = [
        {
            "id": str(audit.id),
            "actor_type": audit.actor_type,
            "actor_id": str(audit.actor_id) if audit.actor_id else None,
            "action": audit.action,
            "entity_type": audit.entity_type,
            "entity_id": str(audit.entity_id) if audit.entity_id else None,
            "metadata": audit.extra_data,
            "created_at": audit.created_at.isoformat() if audit.created_at else None,
        }
        for audit in audits
    ]
    
    return {
        "items": items,
        "count": len(items)
    }
