import hashlib, re, wave
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from pypdf import PdfReader

@dataclass
class ParsedDocument:
    title: str
    pages: list[str]

@dataclass
class CandidateChapter:
    title: str
    content: str
    page_start: int | None = None
    page_end: int | None = None

def normalize_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    return re.sub(r" +", " ", text).strip()

def parse_pdf(path: Path) -> ParsedDocument:
    reader = PdfReader(str(path))
    pages = [normalize_text(page.extract_text() or "") for page in reader.pages]
    title = (reader.metadata.title if reader.metadata and reader.metadata.title else path.stem).strip()
    return ParsedDocument(title=title or "Untitled document", pages=pages)

HEADING = re.compile(r"^(chapter\s+(?:\d+|[ivxlcdm]+)|(?:\d+\.)+\s+.+|part\s+.+)$", re.I)

def detect_chapters(parsed: ParsedDocument) -> list[CandidateChapter]:
    blocks: list[tuple[str, int]] = []
    for page_no, page in enumerate(parsed.pages, 1):
        blocks.extend((line.strip(), page_no) for line in page.splitlines() if line.strip())
    headings = [(i, line, page) for i, (line, page) in enumerate(blocks) if HEADING.match(line) and len(line) <= 120]
    if not headings:
        return [CandidateChapter("Full document", normalize_text("\n".join(text for text, _ in blocks)), 1, len(parsed.pages))]
    result = []
    for index, (start, title, page) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(blocks)
        content = normalize_text("\n".join(text for text, _ in blocks[start + 1:end]))
        result.append(CandidateChapter(title, content, page, headings[index + 1][2] - 1 if index + 1 < len(headings) else len(parsed.pages)))
    return result

def chunk_text(text: str, limit: int = 1800) -> list[str]:
    text = normalize_text(text)
    if not text: return []
    paragraphs = re.split(r"\n\n+", text)
    chunks, current = [], ""
    for paragraph in paragraphs:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        for sentence in sentences:
            if len(current) + len(sentence) + 1 > limit and current:
                chunks.append(current.strip()); current = ""
            if len(sentence) > limit:
                for offset in range(0, len(sentence), limit): chunks.append(sentence[offset:offset + limit].strip())
            else: current = f"{current} {sentence}".strip()
    if current: chunks.append(current)
    return chunks

def mock_wav(text: str) -> tuple[bytes, float]:
    duration = max(1.0, min(30.0, len(text) / 18))
    frames = int(8000 * duration)
    output = BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(8000)
        audio.writeframes(b"\x00\x00" * frames)
    return output.getvalue(), duration

def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
