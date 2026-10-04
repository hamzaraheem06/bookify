# BookPilot — Technology Stack

This document describes the intended baseline stack. It should be kept synchronized with the actual repository before each major milestone.

## Frontend

### React + Vite

Used for the web client and development/build tooling.

### TypeScript

Preferred for stable API/data contracts and safer team development if the existing frontend already uses TypeScript or can be migrated without excessive churn.

### Styling

Use the existing coherent styling approach in the repository. Avoid introducing multiple competing styling systems.

## Backend

### Python 3.11

Preferred baseline runtime for reproducibility and library compatibility.

### FastAPI

Used for HTTP API endpoints, validation, and application integration.

### Pydantic

Used for request/response schemas and configuration validation.

### SQLAlchemy

Used for ORM/database interaction.

### Alembic

Used for database migrations.

## Database

### PostgreSQL

Primary relational database for users, books, chapters, jobs, assets, and playback metadata.

## Document Processing

### Docling

Preferred primary PDF/document parsing implementation, wrapped by the application's parser interface.

If installation/runtime constraints make this impractical for the actual baseline, the chosen fallback parser must be documented here and in the research notes.

## Audio / TTS

### Provider abstraction

The application owns a TTS interface rather than binding the domain to one vendor.

A production-quality external provider such as ElevenLabs may be configured, while a local or deterministic development provider keeps the project usable without a paid API account.

### FFmpeg

Use only where required for audio validation/assembly. If it is part of the implementation, document its installation as a system dependency.

## Storage

### Local development

A filesystem-backed storage adapter is appropriate for local development.

### Future cloud

Use an S3-compatible/cloud object store through the same `StorageProvider` interface.

## Testing

Use a Python testing framework such as `pytest` for backend tests. Frontend testing should use the toolchain already established in the repository; maintain at least build/type/lint checks and focused component tests where practical.

## Infrastructure Philosophy

The semester baseline should avoid mandatory:

- Kubernetes;
- service meshes;
- microservice deployment;
- complex streaming systems;
- paid managed queues;
- multi-region infrastructure.

The goal is a maintainable modular monolith with background processing.

### Implemented V1 parser choice

The current local baseline uses `pypdf` behind the parser abstraction. This keeps fresh-clone installation reliable without making Docling's heavier runtime dependencies mandatory. The internal parse result and downstream services remain library-independent so Docling can be evaluated as a later adapter.
