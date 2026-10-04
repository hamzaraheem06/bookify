# BookPilot — Requirements

## 1. Actors

### Guest

Can access public application pages and the authentication interface, but cannot access private books or processing jobs.

### Authenticated User

Can upload PDFs, manage their own books, review chapters, request generation, listen to generated audiobooks, and manage playback progress.

### System / Worker

Runs long-running document-processing and generation tasks outside normal HTTP request handling.

## 2. Functional Requirements

### FR-01 Authentication

The system shall allow a user to register and log in securely.

### FR-02 Protected Access

Private books, chapters, assets, and jobs shall only be accessible to their owner.

### FR-03 PDF Upload

An authenticated user shall be able to upload a PDF that satisfies the configured type and size limits.

### FR-04 Book Creation

A successful upload shall create a persistent book/document record and processing state.

### FR-05 PDF Parsing

The system shall extract usable text and structural information from supported PDFs.

### FR-06 Structure Detection

The system shall generate candidate chapters/sections in deterministic order where possible.

### FR-07 Structure Review

The user shall be able to review and edit detected chapter titles/order and inclusion before generation.

### FR-08 Text Normalization

The system shall normalize common PDF extraction artifacts while preserving document meaning.

### FR-09 Text Chunking

Large chapter content shall be divided into ordered, TTS-compatible chunks.

### FR-10 Generation Jobs

Audiobook generation shall execute as an asynchronous job with visible state/progress.

### FR-11 Chapter-Level Generation

The system shall generate audio independently for chapters and preserve completed chapters if another chapter fails.

### FR-12 TTS Abstraction

TTS generation shall be accessed through a provider abstraction rather than provider-specific calls embedded in API routes.

### FR-13 Audio Storage

Generated audio assets shall be stored through the application's storage abstraction.

### FR-14 Personal Library

Authenticated users shall be able to view their own books and processing states.

### FR-15 Book Details

The system shall show a book's chapter list, chapter status, and available audio.

### FR-16 Player

The application shall provide a global web audio player with play/pause, seek, volume, speed, chapter navigation, and automatic next-chapter behavior.

### FR-17 Progress

Playback position shall be persisted and restored.

### FR-18 Deletion

Users shall be able to delete their own books subject to correct database/storage cleanup.

### FR-19 Failure Visibility

Processing failures shall be represented explicitly and expose useful user-facing error information.

### FR-20 Retryability

Where practical, failed processing work shall be retryable without unnecessarily regenerating completed work.

## 3. Non-Functional Requirements

### NFR-01 Reliability

The major V1 user journey should complete consistently without requiring manual database changes.

### NFR-02 Maintainability

Responsibilities shall be separated into understandable modules and services suitable for team development.

### NFR-03 Security

Passwords shall be hashed, secrets shall be externalized, and authorization shall be enforced server-side.

### NFR-04 Performance

Long-running parsing and generation work shall not block normal HTTP requests.

### NFR-05 Portability

Local development shall work without mandatory paid cloud infrastructure.

### NFR-06 Extensibility

The system shall expose clean abstractions for parser, TTS, and storage providers.

### NFR-07 Testability

The core processing logic shall be testable without relying on external paid APIs.

### NFR-08 Documentation

The repository shall contain enough setup and architecture information for a new team member to start work independently.

## 4. Constraints

- PDF is the only upload format in V1.
- Semester-project scope limits infrastructure complexity.
- External provider limits may affect TTS generation.
- User-supplied files must be handled within configured storage/file-size limits.
- The project is not intended to provide unlimited free production hosting.

## 5. Acceptance Criteria

The baseline is acceptable when the end-to-end workflow works from a clean database: register → login → upload PDF → parse → review chapters → generate → play → persist progress, with correct ownership enforcement and a reproducible local setup.
