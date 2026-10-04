# BookPilot — Extensibility and Provider Model

## 1. Goal

BookPilot should be extensible without turning V1 into a plugin framework project.

The approach is therefore **simple internal interfaces and provider adapters**, not dynamic third-party plugins.

## 2. Stable Extension Points

The most important seams are:

```text
DocumentParser
StorageProvider
TTSProvider
AudioPostProcessor
```

Additional domain-specific processors can be introduced later if actual requirements justify them.

## 3. Parser Replacement

Core application logic consumes `DocumentParseResult`. A future parser implementation can therefore replace the current parser adapter without forcing changes in book/chapter/generation services.

## 4. TTS Replacement

Core generation logic consumes the `TTSProvider` contract. A future provider only needs to implement the required interface and configuration mapping.

## 5. Storage Replacement

Local development storage and cloud object storage should satisfy the same internal contract.

Conceptually:

```text
                StorageProvider
                 /           \
                /             \
        LocalStorage       CloudStorage
```

## 6. Future RAG

A later RAG pipeline could reuse:

```text
Book / Document
      ↓
Parser
      ↓
Structured Content
      ↓
Chunking
      ↓
Embeddings / Index
      ↓
Retrieval + Answering
```

This does not require modifying the audiobook player's implementation.

## 7. Future Research-Paper Explainers

Another future pipeline could reuse document ingestion and structure understanding and then produce an explanatory artifact instead of audio.

## 8. Avoiding Over-Abstraction

Do not create abstract factories, registries, plugin discovery systems, or dependency-injection frameworks just to satisfy this document.

Abstractions are justified when they protect the application from a concrete replaceable dependency.

## 9. Configuration

Provider selection should be configuration-driven where appropriate, for example:

```text
TTS_PROVIDER=mock
TTS_PROVIDER=elevenlabs
TTS_PROVIDER=qwen3
```

Exact environment variable names should match the actual implementation.

## 10. Semantic Boundary

A useful rule for the team is:

> Core application code knows what it needs; provider adapters know how a specific external technology provides it.
