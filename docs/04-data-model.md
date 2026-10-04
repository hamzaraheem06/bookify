# BookPilot — Data Model

## 1. Entity Overview

```text
User
 │
 └──< Book
       │
       ├──< DocumentAsset
       │
       ├──< ProcessingJob
       │
       ├──< Chapter
       │      │
       │      ├──< ContentChunk
       │      └──< AudioAsset
       │
       └──< PlaybackProgress
```

## 2. User

Represents an authenticated application user.

Suggested fields:

- `id`
- `email`
- `password_hash`
- `created_at`
- `updated_at`

Email should be uniquely constrained.

## 3. Book

Represents the user-facing document/audiobook project.

Suggested fields:

- `id`
- `user_id`
- `title`
- `status`
- optional metadata
- `created_at`
- `updated_at`

A book belongs to exactly one user in V1.

## 4. DocumentAsset

Represents an uploaded source document.

Suggested fields:

- `id`
- `book_id`
- `storage_key`
- `original_filename`
- `mime_type`
- `size_bytes`
- `created_at`

The database stores a reference to the file rather than the complete PDF binary.

## 5. Chapter

Represents an ordered user-facing chapter/section.

Suggested fields:

- `id`
- `book_id`
- `title`
- `sequence_number`
- `content` or a reference to the normalized content representation
- `included`
- `status`
- optional source-page metadata
- `created_at`
- `updated_at`

A uniqueness constraint should prevent duplicate chapter sequence numbers within a book where appropriate.

## 6. ContentChunk

Represents an ordered TTS-ready text segment.

Suggested fields:

- `id`
- `chapter_id`
- `sequence_number`
- `text`
- `status`
- optional text hash/content fingerprint
- `created_at`

## 7. ProcessingJob

Represents a long-running processing operation.

Suggested fields:

- `id`
- `book_id`
- `job_type`
- `status`
- `progress_percent`
- `current_stage`
- `error_message`
- `created_at`
- `started_at`
- `completed_at`

## 8. AudioAsset

Represents a generated audio object.

Suggested fields:

- `id`
- `chapter_id`
- `storage_key`
- `mime_type`
- `duration_seconds`
- `size_bytes`
- optional generation metadata
- `created_at`

Do not store large audio binaries directly in ordinary relational rows.

## 9. PlaybackProgress

Represents a user's position in a book.

Suggested fields:

- `id`
- `user_id`
- `book_id`
- `chapter_id`
- `position_seconds`
- `updated_at`

A uniqueness rule should ensure one active progress record per user/book according to the chosen design.

## 10. Status Design

Use explicit application-level enums/constants for book, chapter, and job states. Avoid arbitrary free-form status strings.

## 11. Ownership and Security

Every private object must be traceable back to a user. Authorization checks must follow the relationship:

```text
requesting user → book → child resource
```

The backend must enforce this relationship for reads, updates, playback asset access, and deletion.

## 12. Migration Principles

The repository must contain a reproducible Alembic migration chain. New team members should never need to inspect an existing developer's local database to infer the schema.
