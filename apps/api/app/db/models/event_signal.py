"""EventSignal model"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from app.db.base import Base, UUIDMixin, TimestampMixin


class EventSignal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "event_signals"
    
    asset_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    impact_score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    direction: Mapped[str | None] = mapped_column(String(20))
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    source_ref: Mapped[str | None] = mapped_column(String(500))
    extra_data: Mapped[dict] = mapped_column(JSON, default=dict)
