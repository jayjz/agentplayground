"""Audit logs API - DB-backed implementation."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audit_log import AuditLog
from app.db.session import get_session

router = APIRouter()


def serialize_audit(audit: AuditLog) -> dict[str, Any]:
    """Serialize an AuditLog ORM object into a JSON-safe dictionary."""
    return {
        "id": str(audit.id),
        "actor_type": audit.actor_type,
        "actor_id": str(audit.actor_id) if audit.actor_id else None,
        "action": audit.action,
        "entity_type": audit.entity_type,
        "entity_id": str(audit.entity_id) if audit.entity_id else None,
        "metadata": audit.extra_data or {},
        "created_at": audit.created_at.isoformat() if audit.created_at else None,
    }


@router.get("/")
async def list_audits(
    db: AsyncSession = Depends(get_session),
    action: str | None = Query(default=None, description="Filter by audit action"),
    entity_type: str | None = Query(default=None, description="Filter by entity type"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of audit logs to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
) -> dict[str, Any]:
    """List audit logs from the database with optional filtering."""
    stmt: Select[tuple[AuditLog]] = select(AuditLog)

    if action:
        stmt = stmt.where(AuditLog.action == action)

    if entity_type:
        stmt = stmt.where(AuditLog.entity_type == entity_type)

    stmt = (
        stmt.order_by(AuditLog.created_at.desc().nullslast())
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(stmt)
    audits = result.scalars().all()

    items = [serialize_audit(audit) for audit in audits]

    return {
        "items": items,
        "count": len(items),
    }
