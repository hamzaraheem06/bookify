from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from ...api.deps import current_user
from ...core.config import settings
from ...core.database import get_db
from ...models import Book, BookStatus, Chapter, ChapterStatus, DocumentAsset, JobStatus, JobType, ProcessingJob, User
from ...services.storage import storage
router = APIRouter(prefix="/books", tags=["books"])
class ChapterUpdate(BaseModel): title: str = Field(min_length=1, max_length=240); sequence_number: int = Field(ge=1); included: bool = True; content: str = Field(min_length=1)
class ChapterOut(BaseModel): id: int; title: str; sequence_number: int; content: str; included: bool; status: str; duration_seconds: float | None = None; audio_url: str | None = None
class BookOut(BaseModel): id: int; title: str; status: str; error_message: str | None; created_at: str; chapters: list[ChapterOut]; generation_progress: int = 0
def owned(db: Session, user_id: int, book_id: int) -> Book:
    book = db.scalar(select(Book).options(selectinload(Book.chapters).selectinload(Chapter.audio_asset), selectinload(Book.jobs), selectinload(Book.source_asset)).where(Book.id == book_id, Book.user_id == user_id))
    if not book: raise HTTPException(404, "Book not found")
    return book
def serialize(book: Book) -> BookOut:
    job = book.jobs[-1] if book.jobs else None
    return BookOut(id=book.id, title=book.title, status=book.status.value, error_message=book.error_message, created_at=book.created_at.isoformat(), generation_progress=job.progress_percent if job and job.job_type == JobType.GENERATION else 0, chapters=[ChapterOut(id=c.id, title=c.title, sequence_number=c.sequence_number, content=c.content, included=c.included, status=c.status.value, duration_seconds=c.audio_asset.duration_seconds if c.audio_asset else None, audio_url=f"/api/assets/audio/{c.audio_asset.id}" if c.audio_asset else None) for c in book.chapters])
@router.post("", response_model=BookOut, status_code=201)
async def upload_pdf(file: UploadFile = File(...), user: User = Depends(current_user), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf" and not (file.filename or "").lower().endswith(".pdf"): raise HTTPException(415, "Only PDF uploads are supported")
    data = await file.read()
    if not data or len(data) > settings.max_upload_bytes: raise HTTPException(413, "PDF is empty or exceeds the upload limit")
    key = f"sources/{user.id}/{uuid4().hex}.pdf"; storage.put(key, data)
    book = Book(user_id=user.id, title=Path(file.filename or "document.pdf").stem, status=BookStatus.UPLOADED); db.add(book); db.flush()
    book.source_asset = DocumentAsset(book_id=book.id, storage_key=key, original_filename=file.filename or "document.pdf", mime_type="application/pdf", size_bytes=len(data)); db.add(ProcessingJob(book_id=book.id, job_type=JobType.INGESTION, status=JobStatus.QUEUED)); db.commit()
    return serialize(owned(db, user.id, book.id))
@router.get("", response_model=list[BookOut])
def list_books(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [serialize(book) for book in db.scalars(select(Book).options(selectinload(Book.chapters).selectinload(Chapter.audio_asset), selectinload(Book.jobs), selectinload(Book.source_asset)).where(Book.user_id == user.id).order_by(Book.created_at.desc())).unique().all()]
@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)): return serialize(owned(db, user.id, book_id))
@router.put("/{book_id}/chapters", response_model=BookOut)
def update_chapters(book_id: int, payload: list[ChapterUpdate], user: User = Depends(current_user), db: Session = Depends(get_db)):
    book = owned(db, user.id, book_id)
    if book.status not in (BookStatus.REVIEW_REQUIRED, BookStatus.READY_FOR_GENERATION): raise HTTPException(409, "Book is not in review")
    for chapter, update in zip(sorted(book.chapters, key=lambda item: item.sequence_number), sorted(payload, key=lambda item: item.sequence_number)):
        chapter.title, chapter.sequence_number, chapter.included, chapter.content, chapter.status = update.title, update.sequence_number, update.included, update.content, ChapterStatus.REVIEWED
    book.status = BookStatus.READY_FOR_GENERATION; db.commit(); return serialize(owned(db, user.id, book_id))
@router.post("/{book_id}/generation", response_model=BookOut)
def generate(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    book = owned(db, user.id, book_id)
    if book.status not in (BookStatus.READY_FOR_GENERATION, BookStatus.COMPLETED, BookStatus.FAILED): raise HTTPException(409, "Book is not ready for generation")
    db.add(ProcessingJob(book_id=book.id, job_type=JobType.GENERATION, status=JobStatus.QUEUED)); book.status = BookStatus.GENERATING; db.commit(); return serialize(owned(db, user.id, book_id))
@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    book = owned(db, user.id, book_id); source = book.source_asset.storage_key if book.source_asset else None; db.delete(book); db.commit();
    if source: storage.delete(source)
