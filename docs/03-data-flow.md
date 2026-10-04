# BookPilot — Data Flow

## 1. End-to-End Flow

```text
[User]
  |
  | PDF upload
  v
[FastAPI API]
  |
  +--> validate extension/MIME/size
  |
  +--> create Book + DocumentAsset + Job
  |
  v
[StorageProvider]
  |
  | source PDF reference
  v
[Background Worker]
  |
  v
[DocumentParser]
  |
  +--> title / metadata
  +--> pages / blocks / text
  +--> structural headings
  |
  v
[StructureDetector]
  |
  +--> candidate chapters/sections
  |
  v
[Database]
  |
  v
[Frontend Review UI]
  |
  | user edits/approves
  v
[Normalized Chapters]
  |
  v
[TextNormalizer]
  |
  v
[TextChunker]
  |
  v
[GenerationJob]
  |
  v
[TTSProvider]
  |
  +--> chunk audio
  |
  v
[AudioPostProcessor]
  |
  +--> chapter audio
  |
  v
[StorageProvider]
  |
  v
[AudioAsset records]
  |
  v
[Book Details / Player]
  |
  v
[PlaybackProgress]
```

## 2. Book State Flow

```text
UPLOADED
   ↓
PROCESSING
   ↓
REVIEW_REQUIRED
   ↓
READY_FOR_GENERATION
   ↓
GENERATING
   ↓
COMPLETED
```

Any processing stage may transition to `FAILED` with a diagnostic message. Recovery should preserve useful existing state.

## 3. Upload Flow

The backend should validate the request before creating long-running work. The source PDF is stored and referenced by a `DocumentAsset` record. The source file should not be copied into arbitrary application directories using user-controlled names.

## 4. Parsing Flow

A parser adapter reads the source document and produces a normalized parse result. The parse result may include page-level information and structural hints. Structure detection then creates candidate chapters.

## 5. Review Flow

The frontend obtains candidate chapters from the backend. The user can edit titles, ordering, inclusion, and appropriate text/content fields. The server persists approved structure before generation begins.

## 6. Generation Flow

A generation request creates a job. The worker resolves the approved chapters, normalizes/chunks text, invokes the selected TTS provider, stores chunk/chapter assets, and updates job progress.

Chapter-level isolation means a failure in Chapter 7 does not require Chapters 1–6 to be regenerated.

## 7. Playback Flow

The frontend retrieves chapter metadata and audio references through the API. The browser's native audio facilities perform playback. Progress updates are sent to the backend periodically and at important lifecycle events such as pause, chapter change, and page unload where practical.

## 8. Error Flow

Errors should be recorded at the appropriate scope:

- book-level: parsing or source failure;
- chapter-level: a specific chapter cannot be processed;
- job-level: orchestration failure;
- provider-level: external TTS/storage failure.

User-facing messages should remain understandable and should not expose stack traces or credentials.
