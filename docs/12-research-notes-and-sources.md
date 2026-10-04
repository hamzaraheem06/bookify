# BookPilot — Research Notes and Sources

This document records sources and decisions relevant to the baseline architecture. Prefer official technical documentation for implementation details and re-check provider capabilities before production use.

## 1. FastAPI

Official documentation:
https://fastapi.tiangolo.com/

Used as the backend API framework.

## 2. React

Official documentation:
https://react.dev/

Used for the web frontend.

## 3. Vite

Official documentation:
https://vite.dev/

Used for frontend development/build tooling.

## 4. SQLAlchemy

Official documentation:
https://docs.sqlalchemy.org/

Used for relational database access/ORM.

## 5. Alembic

Official documentation:
https://alembic.sqlalchemy.org/

Used for reproducible schema migrations.

## 6. PostgreSQL

Official documentation:
https://www.postgresql.org/docs/

Used as the primary relational database.

## 7. Docling

Official project/documentation:
https://github.com/docling-project/docling

Docling is the preferred document-parsing/understanding implementation for the baseline when environment compatibility is acceptable. BookPilot should keep it behind a parser abstraction so that its internal model does not depend on Docling-specific classes.

## 8. ElevenLabs

Official documentation:
https://elevenlabs.io/docs

A high-quality external TTS provider can be integrated behind the `TTSProvider` abstraction. Provider capabilities, quotas, pricing, licensing, and model availability must be re-checked before a hosted deployment.

## 9. Qwen3-TTS

Official model/project source:
https://github.com/QwenLM/Qwen3-TTS

Qwen3-TTS is a potential local/self-hosted provider path where hardware and licensing/environment constraints permit. It should remain an adapter rather than a hard dependency of the application core.

## 10. MDN Web Audio Element

https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/audio

The web player should use standard browser audio capabilities rather than inventing a custom media transport layer for V1.

## 11. Architectural Conclusions

The key design conclusions are:

1. A modular monolith is appropriate for the semester scope.
2. Long-running PDF/TTS work should be backgrounded.
3. Parser, TTS, and storage dependencies should be abstracted.
4. Chapter detection should be reviewable rather than assumed perfect.
5. Chapter-level audio improves fault isolation and playback organization.
6. Local development should remain possible without paid provider infrastructure.
7. The document model should be reusable by future RAG/research pipelines.

## 12. Research Discipline

When an implementation decision depends on a provider feature, pricing tier, model limit, license, or hosted-service quota, verify the current official documentation before relying on it. Do not encode assumptions about third-party services permanently into core domain logic.

## 13. Implemented Baseline Decisions

V1 uses a local filesystem storage adapter, a deterministic mock WAV provider, and a `pypdf` parser adapter. These choices preserve the documented provider boundaries while keeping local development free of paid credentials and heavyweight optional runtime dependencies. A production TTS adapter and Docling adapter can be added behind the same interfaces after the stable semester journey is validated.
