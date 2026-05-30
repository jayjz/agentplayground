"""Audit service for writing immutable audit logs"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.audit_log import AuditLog
import uuid


async def write_audit(
    db: AsyncSession,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    actor_type: str = "system",
    actor_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    """Write an audit log entry"""
    audit_log = AuditLog(
        actor_type=actor_type,
        actor_id=uuid.UUID(actor_id) if actor_id else None,
        action=action,
        entity_type=entity_type,
        entity_id=uuid.UUID(entity_id) if entity_id else None,
        metadata=metadata or {},
    )
    db.add(audit_log)
    await db.flush()
    return audit_log
