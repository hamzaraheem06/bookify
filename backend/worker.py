from datetime import datetime
import time
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models import AudioAsset, Book, BookStatus, Chapter, ChapterStatus, ChunkStatus, ContentChunk, JobStatus, JobType, ProcessingJob
from app.services.pipeline import chunk_text, detect_chapters, fingerprint, mock_wav, parse_pdf
from app.services.storage import storage

def process_once() -> bool:
    db = SessionLocal(); job = db.scalar(select(ProcessingJob).where(ProcessingJob.status == JobStatus.QUEUED).order_by(ProcessingJob.created_at))
    if not job: db.close(); return False
    book = db.get(Book, job.book_id); job.status = JobStatus.RUNNING; job.started_at = datetime.utcnow(); book.status = BookStatus.PROCESSING if job.job_type == JobType.INGESTION else BookStatus.GENERATING; db.commit()
    try:
        if job.job_type == JobType.INGESTION:
            parsed = parse_pdf(storage.path(book.source_asset.storage_key), book.source_asset.original_filename); book.title = parsed.title
            for index, item in enumerate(detect_chapters(parsed), 1): db.add(Chapter(book_id=book.id, title=item.title, sequence_number=index, content=item.content, source_page_start=item.page_start, source_page_end=item.page_end))
            book.status = BookStatus.REVIEW_REQUIRED; job.current_stage = "review"; job.progress_percent = 100
        else:
            chapters = [c for c in book.chapters if c.included and (c.status != ChapterStatus.COMPLETED or not c.audio_asset)]; total = max(1, len(chapters))
            for index, chapter in enumerate(chapters, 1):
                chapter.status = ChapterStatus.GENERATING; db.flush(); chunks = chunk_text(chapter.content); chapter.chunks.clear()
                for seq, text in enumerate(chunks, 1): db.add(ContentChunk(chapter_id=chapter.id, sequence_number=seq, text=text, content_hash=fingerprint(text), status=ChunkStatus.GENERATED))
                audio, duration = mock_wav(chapter.content); key = f"audio/{book.user_id}/{book.id}/{chapter.id}.wav"; storage.put(key, audio)
                chapter.audio_asset = AudioAsset(storage_key=key, duration_seconds=duration, size_bytes=len(audio)); chapter.status = ChapterStatus.COMPLETED; job.progress_percent = int(index / total * 100); job.current_stage = f"chapter {index} of {total}"; db.commit()
            book.status = BookStatus.COMPLETED
        job.status = JobStatus.COMPLETED; job.completed_at = datetime.utcnow(); db.commit()
    except Exception as exc:
        db.rollback(); job = db.get(ProcessingJob, job.id); book = db.get(Book, job.book_id); job.status = JobStatus.FAILED; job.error_message = str(exc)[:500]; book.status = BookStatus.FAILED; book.error_message = job.error_message; db.commit()
    finally: db.close()
    return True

if __name__ == "__main__":
    while True:
        if not process_once():
            time.sleep(1)
