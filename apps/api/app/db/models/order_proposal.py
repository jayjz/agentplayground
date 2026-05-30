"""OrderProposal model"""
from sqlalchemy import String, Text, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, UUIDMixin, TimestampMixin


class OrderProposal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "order_proposals"
    __table_args__ = {"schema": "portfolio"}
    
    trade_candidate_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("portfolio.trade_candidates.id"), nullable=False)
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("market_data.assets.id"), nullable=False)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order_type: Mapped[str] = mapped_column(String(20), nullable=False)
    limit_price: Mapped[float | None] = mapped_column(Numeric(20, 6))
    status: Mapped[str] = mapped_column(String(30), default="proposed", nullable=False)
    execution_mode: Mapped[str] = mapped_column(String(20), default="paper", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
