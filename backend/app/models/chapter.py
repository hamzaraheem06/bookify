from datetime import datetime
from enum import StrEnum
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base

class ChapterStatus(StrEnum):
    DETECTED = "DETECTED"
    REVIEWED = "REVIEWED"
    QUEUED = "QUEUED"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Chapter(Base):
    __tablename__ = "chapters"
    __table_args__ = (UniqueConstraint("book_id", "sequence_number", name="uq_chapter_book_sequence"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(240))
    sequence_number: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text, default="")
    included: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[ChapterStatus] = mapped_column(Enum(ChapterStatus), default=ChapterStatus.DETECTED)
    source_page_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_page_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    book = relationship("Book", back_populates="chapters")
    chunks = relationship("ContentChunk", back_populates="chapter", cascade="all, delete-orphan", order_by="ContentChunk.sequence_number")
    audio_asset = relationship("AudioAsset", back_populates="chapter", uselist=False, cascade="all, delete-orphan")
