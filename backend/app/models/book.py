from datetime import datetime
from enum import StrEnum
from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base

class BookStatus(StrEnum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    READY_FOR_GENERATION = "READY_FOR_GENERATION"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (Index("ix_books_owner_status", "user_id", "status"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(240), default="Untitled document")
    status: Mapped[BookStatus] = mapped_column(Enum(BookStatus), default=BookStatus.UPLOADED, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="books")
    source_asset = relationship("DocumentAsset", back_populates="book", uselist=False, cascade="all, delete-orphan")
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan", order_by="Chapter.sequence_number")
    jobs = relationship("ProcessingJob", back_populates="book", cascade="all, delete-orphan", order_by="ProcessingJob.created_at")
    playback_progress = relationship("PlaybackProgress", back_populates="book", cascade="all, delete-orphan")
