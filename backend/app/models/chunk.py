from datetime import datetime
from enum import StrEnum
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base

class ChunkStatus(StrEnum):
    READY = "READY"
    GENERATED = "GENERATED"
    FAILED = "FAILED"

class ContentChunk(Base):
    __tablename__ = "content_chunks"
    __table_args__ = (UniqueConstraint("chapter_id", "sequence_number", name="uq_chunk_chapter_sequence"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), index=True)
    sequence_number: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64))
    status: Mapped[ChunkStatus] = mapped_column(Enum(ChunkStatus), default=ChunkStatus.READY)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    chapter = relationship("Chapter", back_populates="chunks")
