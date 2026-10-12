from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from ...api.deps import current_user
from ...core.database import get_db
from ...models import Book, Chapter, PlaybackProgress, User
router = APIRouter(prefix="/player", tags=["player"])
class ProgressIn(BaseModel): chapter_id: int | None = None; position_seconds: float = Field(ge=0)
class ProgressOut(ProgressIn): book_id: int; updated_at: str
class HistoryOut(BaseModel):
    book_id: int
    title: str
    cover_url: str | None = None
    chapter_id: int | None
    chapter_title: str | None
    position_seconds: float
    completed_seconds: float
    total_seconds: float
    percentage: float
    last_listened_at: str
@router.get("/{book_id}/progress", response_model=ProgressOut | None)
def get_progress(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    row = db.scalar(select(PlaybackProgress).where(PlaybackProgress.book_id == book_id, PlaybackProgress.user_id == user.id)); return ProgressOut(book_id=row.book_id, chapter_id=row.chapter_id, position_seconds=row.position_seconds, updated_at=row.updated_at.isoformat()) if row else None
@router.put("/{book_id}/progress", response_model=ProgressOut)
def save_progress(book_id: int, payload: ProgressIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.scalar(select(Book).where(Book.id == book_id, Book.user_id == user.id)): raise HTTPException(404, "Book not found")
    if payload.chapter_id and not db.scalar(select(Chapter).where(Chapter.id == payload.chapter_id, Chapter.book_id == book_id)): raise HTTPException(400, "Chapter does not belong to book")
    row = db.scalar(select(PlaybackProgress).where(PlaybackProgress.book_id == book_id, PlaybackProgress.user_id == user.id)) or PlaybackProgress(user_id=user.id, book_id=book_id)
    row.chapter_id, row.position_seconds = payload.chapter_id, payload.position_seconds; db.add(row); db.commit(); db.refresh(row); return ProgressOut(book_id=row.book_id, chapter_id=row.chapter_id, position_seconds=row.position_seconds, updated_at=row.updated_at.isoformat())

def history_item(row: PlaybackProgress) -> HistoryOut:
    book = row.book
    total = sum((chapter.audio_asset.duration_seconds if chapter.audio_asset else 0) for chapter in book.chapters)
    completed = row.position_seconds
    if row.chapter:
        completed += sum((chapter.audio_asset.duration_seconds if chapter.audio_asset else 0) for chapter in book.chapters if chapter.sequence_number < row.chapter.sequence_number)
    percentage = min(100.0, max(0.0, completed / total * 100)) if total else 0
    return HistoryOut(book_id=book.id, title=book.title, chapter_id=row.chapter_id, chapter_title=row.chapter.title if row.chapter else None, position_seconds=row.position_seconds, completed_seconds=completed, total_seconds=total, percentage=percentage, last_listened_at=row.updated_at.isoformat())

@router.get("/history", response_model=list[HistoryOut])
def get_history(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(PlaybackProgress).options(selectinload(PlaybackProgress.book).selectinload(Book.chapters).selectinload(Chapter.audio_asset), selectinload(PlaybackProgress.chapter)).where(PlaybackProgress.user_id == user.id).order_by(PlaybackProgress.updated_at.desc())).all()
    return [history_item(row) for row in rows]

@router.get("/history/{book_id}", response_model=HistoryOut | None)
def get_book_history(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    row = db.scalar(select(PlaybackProgress).options(selectinload(PlaybackProgress.book).selectinload(Book.chapters).selectinload(Chapter.audio_asset), selectinload(PlaybackProgress.chapter)).where(PlaybackProgress.user_id == user.id, PlaybackProgress.book_id == book_id))
    return history_item(row) if row else None
