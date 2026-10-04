# BookPilot — Architecture

## 1. Architecture Style

BookPilot uses a **modular monolith**. The application remains one deployable backend system, but internal responsibilities are separated into modules and services.

This is intentional for a semester project: it keeps deployment and development simple while preventing the codebase from becoming a single undifferentiated application.

## 2. High-Level Architecture

```text
┌───────────────────────────────┐
│        React + Vite           │
│  Pages / Features / Player    │
└───────────────┬───────────────┘
                │ HTTP / API
                ▼
┌───────────────────────────────┐
│           FastAPI             │
│ Auth / Books / Jobs / Player  │
└───────────────┬───────────────┘
                │
       ┌────────┼─────────┐
       ▼        ▼         ▼
┌──────────┐ ┌───────┐ ┌─────────────┐
│ Services │ │   DB  │ │   Storage   │
│ /Domain  │ │Postgres│ │ Provider    │
└────┬─────┘ └───────┘ └─────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ Background Worker / Job Runner  │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│       Document Pipeline         │
│ Parse → Structure → Normalize   │
│       → Chunk → Generate        │
└───────┬───────────────┬─────────┘
        ▼               ▼
  Document Parser      TTS Provider
```

## 3. Backend Layers

### API Layer

FastAPI routes are responsible for HTTP concerns:

- request validation;
- authentication dependencies;
- authorization checks;
- invoking application services; and
- serializing responses.

Routes should remain thin.

### Service Layer

Services contain use-case/business logic such as:

- user/account operations;
- book management;
- ingestion;
- chapter review;
- generation orchestration;
- playback progress.

### Pipeline Layer

Pipeline modules process documents and generation artifacts in distinct stages.

### Data Layer

SQLAlchemy models, repositories/helpers where needed, and Alembic migrations manage persistent state.

### Infrastructure Layer

Provider adapters implement integrations such as:

- local/cloud storage;
- PDF parser;
- TTS service.

## 4. Core Abstractions

### DocumentParser

```text
parse(source) -> DocumentParseResult
```

The rest of BookPilot consumes a normalized internal representation, not raw parser-specific objects.

### TTSProvider

```text
synthesize(text, configuration) -> AudioResult
```

The provider adapter owns API-specific details.

### StorageProvider

```text
put()
get()/download()
delete()
exists()
```

The application should be able to switch between local development storage and a cloud/S3-compatible implementation.

## 5. Background Processing

Parsing and generation can take longer than a normal HTTP request should remain open. The API therefore creates a job and returns a stable job/book state while a worker performs the processing.

The worker should be idempotent where practical and update database state as it progresses.

## 6. Architectural Rules

1. Do not place business logic directly in route functions.
2. Do not call third-party TTS APIs from frontend code.
3. Do not expose raw database models as a public API contract.
4. Do not let parser-specific output leak into all downstream modules.
5. Do not let the frontend own processing truth; the backend/database does.
6. Do not store large generated audio blobs directly in ordinary relational rows.
7. Keep future RAG/research capabilities out of V1 implementations.

## 7. Future Extension Point

The architecture is intentionally compatible with additional pipelines later:

```text
Canonical Document
      ↓
Parsed/Structured Representation
      ↓
 ┌──────────────┬────────────────┬──────────────────┐
 │ Audiobook    │ RAG            │ Research Explain │
 └──────────────┴────────────────┴──────────────────┘
```

Those pipelines can share ingestion/parsing but own their downstream processing.
