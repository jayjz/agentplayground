"""FactorSignal model"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, UUIDMixin, TimestampMixin


class FactorSignal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "factor_signals"
    __table_args__ = {"schema": "research"}
    
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("market_data.assets.id"), nullable=False, index=True)
    signal_date: Mapped[datetime] = mapped_column(Date, nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    raw_value: Mapped[float | None] = mapped_column(Numeric(20, 8))
    normalized_value: Mapped[float | None] = mapped_column(Numeric(20, 8))
    score: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    horizon: Mapped[str | None] = mapped_column(String(20))
    rationale: Mapped[str | None] = mapped_column(Text)
