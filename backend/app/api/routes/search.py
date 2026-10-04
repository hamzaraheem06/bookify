from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ...api.deps import current_user
from ...core.database import get_db
from ...models import Book, Chapter, User
from .books import serialize

router = APIRouter(prefix="/search", tags=["search"])

@router.get("")
def search_books(q: str = Query(default="", max_length=120), user: User = Depends(current_user), db: Session = Depends(get_db)):
    statement = select(Book).options(selectinload(Book.chapters).selectinload(Chapter.audio_asset), selectinload(Book.jobs)).where(Book.user_id == user.id).order_by(Book.created_at.desc())
    term = q.strip()
    if term:
        statement = statement.where(Book.title.ilike(f"%{term}%"))
    return [serialize(book) for book in db.scalars(statement).unique().all()]
