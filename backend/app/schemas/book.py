from pydantic import BaseModel, ConfigDict


class AuthorOut(BaseModel):
    id: int
    name: str
    bio: str
    model_config = ConfigDict(from_attributes=True)


class ChapterOut(BaseModel):
    id: int
    book_id: int
    chapter_number: int
    title: str
    audio_url: str
    duration_seconds: float
    model_config = ConfigDict(from_attributes=True)


class BookOut(BaseModel):
    id: int
    title: str
    description: str
    cover_url: str
    language: str
    publication_year: int
    source: str
    category: str
    author: AuthorOut
    chapters: list[ChapterOut] = []
    model_config = ConfigDict(from_attributes=True)
