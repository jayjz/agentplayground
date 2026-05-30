"""Filing model"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from app.db.base import Base, UUIDMixin, TimestampMixin


class Filing(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "filings"
    
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    filing_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    filing_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    accession_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content_text: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(String(1000))
    parsed_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
