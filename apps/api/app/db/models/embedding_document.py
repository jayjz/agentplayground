"""EmbeddingDocument model"""
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from app.db.base import Base, UUIDMixin, TimestampMixin


class EmbeddingDocument(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "embedding_documents"
    __table_args__ = {"schema": "research"}
    
    document_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_entity_type: Mapped[str | None] = mapped_column(String(100))
    source_entity_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True))
    chunk_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536))
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
