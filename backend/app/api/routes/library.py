from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ...api.deps import current_user
from ...core.database import get_db
from ...models import Book, Chapter, User
from .books import serialize

router = APIRouter(prefix="/library", tags=["library"])

@router.get("")
def list_library(user: User = Depends(current_user), db: Session = Depends(get_db)):
    books = db.scalars(select(Book).options(selectinload(Book.chapters).selectinload(Chapter.audio_asset), selectinload(Book.jobs)).where(Book.user_id == user.id).order_by(Book.created_at.desc())).unique().all()
    return [serialize(book) for book in books]

@router.post("/{book_id}")
def add_to_library(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    book = db.scalar(select(Book).where(Book.id == book_id, Book.user_id == user.id))
    if not book:
        raise HTTPException(404, "Book not found")
    return serialize(book)

@router.delete("/{book_id}", status_code=204)
def remove_from_library(book_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    book = db.scalar(select(Book).where(Book.id == book_id, Book.user_id == user.id))
    if not book:
        raise HTTPException(404, "Book not found")
    db.delete(book)
    db.commit()
