"""NewsItem model"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from app.db.base import Base, UUIDMixin, TimestampMixin


class NewsItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "news_items"
    
    asset_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), index=True)
    headline: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1000))
    sentiment: Mapped[float | None] = mapped_column()
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
