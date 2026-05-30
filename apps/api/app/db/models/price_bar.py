"""PriceBar model"""
from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, UUIDMixin


class PriceBar(Base, UUIDMixin):
    __tablename__ = "price_bars"
    __table_args__ = {"schema": "market_data"}
    
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("market_data.assets.id"), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    open: Mapped[float] = mapped_column(Numeric(20, 6), nullable=False)
    high: Mapped[float] = mapped_column(Numeric(20, 6), nullable=False)
    low: Mapped[float] = mapped_column(Numeric(20, 6), nullable=False)
    close: Mapped[float] = mapped_column(Numeric(20, 6), nullable=False)
    volume: Mapped[int] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
