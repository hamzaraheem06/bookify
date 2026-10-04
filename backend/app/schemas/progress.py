from datetime import datetime
from pydantic import BaseModel


class ProgressUpdate(BaseModel):
    chapter_id: int
    position_seconds: float


class ProgressOut(ProgressUpdate):
    book_id: int
    updated_at: datetime
    completed: bool = False
    last_listened_at: datetime


class HistoryOut(BaseModel):
    book_id: int
    title: str
    cover_url: str
    chapter_id: int | None
    chapter_title: str | None
    position_seconds: float
    completed_seconds: float
    total_seconds: float
    percentage: float
    last_listened_at: datetime
