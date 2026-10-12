def headers(token): return {"Authorization": f"Bearer {token}"}

def test_auth_and_protected_access(client, auth):
    assert client.get("/api/books").status_code == 401
    assert client.get("/api/books", headers=headers(auth)).json() == []

def test_upload_rejects_non_pdf(client, auth):
    response = client.post("/api/books", headers=headers(auth), files={"file": ("notes.txt", b"hello", "text/plain")})
    assert response.status_code == 415

def test_upload_creates_owned_book(client, auth):
    response = client.post("/api/books", headers=headers(auth), files={"file": ("sample.pdf", b"%PDF-1.4\n", "application/pdf")})
    assert response.status_code == 201
    book = response.json(); assert book["status"] == "UPLOADED"; assert book["title"] == "sample"

def test_pipeline_helpers():
    from app.services.pipeline import ParsedDocument, chunk_text, detect_chapters, normalize_text
    assert normalize_text("Hello\nworld") == "Hello world"
    chunks = chunk_text("Sentence one. " * 300, limit=100)
    assert len(chunks) > 1 and "Sentence" in "".join(chunks)
    chapters = detect_chapters(ParsedDocument("Demo", ["Chapter 1\nFirst chapter text\nChapter 2\nSecond chapter text"]))
    assert [chapter.title for chapter in chapters] == ["Chapter 1", "Chapter 2"]
    assert "First chapter text" in chapters[0].content

def test_retry_requeues_failed_job(client, auth):
    from sqlalchemy import select
    from app.core.database import SessionLocal
    from app.models import Book, BookStatus, JobStatus, JobType, ProcessingJob, User
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "owner@example.com"))
        book = Book(user_id=user.id, title="Retry demo", status=BookStatus.FAILED)
        db.add(book); db.flush()
        job = ProcessingJob(book_id=book.id, job_type=JobType.INGESTION, status=JobStatus.FAILED, error_message="temporary")
        db.add(job); db.commit(); book_id = book.id; job_id = job.id
    result = client.post(f"/api/books/{book_id}/retry", headers=headers(auth))
    assert result.status_code == 200 and result.json()["status"] == "UPLOADED"
    with SessionLocal() as db:
        job = db.get(ProcessingJob, job_id)
        assert job.status == JobStatus.QUEUED and job.error_message is None

def test_progress_history_is_available_and_owner_scoped(client, auth):
    from sqlalchemy import select
    from app.core.database import SessionLocal
    from app.models import Book, Chapter, User
    other = client.post("/api/auth/register", json={"email":"other@example.com", "password":"password123"}).json()["token"]
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "owner@example.com"))
        book = Book(user_id=user.id, title="Progress demo")
        db.add(book); db.flush()
        chapter = Chapter(book_id=book.id, title="Chapter 1", sequence_number=1, content="text")
        db.add(chapter); db.commit(); book_id, chapter_id = book.id, chapter.id
    saved = client.put(f"/api/player/{book_id}/progress", headers=headers(auth), json={"chapter_id":chapter_id,"position_seconds":3.5})
    assert saved.status_code == 200
    assert client.get("/api/player/history", headers=headers(auth)).json()[0]["book_id"] == book_id
    assert client.get(f"/api/player/{book_id}/progress", headers=headers(other)).json() is None

def test_book_delete_removes_source_and_audio_files(client, auth):
    from sqlalchemy import select
    from app.core.database import SessionLocal
    from app.models import AudioAsset, Book, Chapter, DocumentAsset, User
    from app.services.storage import storage
    source_key, audio_key = "qa-cleanup/source.pdf", "qa-cleanup/chapter.wav"
    storage.put(source_key, b"source"); storage.put(audio_key, b"audio")
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "owner@example.com"))
        book = Book(user_id=user.id, title="Cleanup demo")
        db.add(book); db.flush()
        book.source_asset = DocumentAsset(book_id=book.id, storage_key=source_key, original_filename="source.pdf", mime_type="application/pdf", size_bytes=6)
        chapter = Chapter(book_id=book.id, title="Chapter 1", sequence_number=1, content="text")
        db.add(chapter); db.flush()
        chapter.audio_asset = AudioAsset(chapter_id=chapter.id, storage_key=audio_key, size_bytes=5, duration_seconds=1)
        db.commit(); book_id = book.id
    response = client.delete(f"/api/books/{book_id}", headers=headers(auth))
    assert response.status_code == 204
    assert not storage.path(source_key).exists() and not storage.path(audio_key).exists()
