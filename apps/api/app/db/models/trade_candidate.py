"""TradeCandidate model"""
from sqlalchemy import String, Text, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from app.db.base import Base, UUIDMixin, TimestampMixin


class TradeCandidate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "trade_candidates"
    
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    thesis: Mapped[str] = mapped_column(Text, nullable=False)
    conviction: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    expected_horizon_days: Mapped[int] = mapped_column(Integer, nullable=False)
    expected_return_bps: Mapped[float | None] = mapped_column(Numeric(10, 4))
    risk_summary: Mapped[str] = mapped_column(Text, nullable=False)
    hedge_symbol: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="pending_review", nullable=False, index=True)
    created_by_agent: Mapped[str] = mapped_column(String(100), nullable=False)
    extra_data: Mapped[dict] = mapped_column(JSON, default=dict)
