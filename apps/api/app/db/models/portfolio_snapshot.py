"""PortfolioSnapshot model"""
from datetime import datetime
from sqlalchemy import DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base, UUIDMixin


class PortfolioSnapshot(Base, UUIDMixin):
    __tablename__ = "portfolio_snapshots"
    __table_args__ = {"schema": "portfolio"}
    
    snapshot_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    gross_exposure: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    net_exposure: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    long_exposure: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    short_exposure: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    sector_breakdown: Mapped[dict] = mapped_column(JSONB, default=dict)
    beta_estimate: Mapped[float | None] = mapped_column(Numeric(10, 6))
    concentration_metrics: Mapped[dict] = mapped_column(JSONB, default=dict)
    notes: Mapped[str | None] = mapped_column()
