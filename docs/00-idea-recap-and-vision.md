# BookPilot — Idea Recap and Product Vision

## 1. Product Summary

**BookPilot** is a document-to-audiobook platform. Version 1 focuses on one clear workflow: a user uploads a PDF book, BookPilot understands its structure, the user reviews the detected chapters, and the system generates a chapter-organized audiobook that can be played through the web application.

The product is intentionally being built as a reusable **document ingestion → understanding → processing → generation → consumption** platform rather than as a one-off audiobook script.

## 2. Core Problem

A user may own or legally have access to a PDF book but still prefer listening instead of reading. Existing audiobook ecosystems are primarily catalog/distribution products. BookPilot instead focuses on transforming a user's own document into a usable audiobook.

The project therefore concentrates on:

- reliable PDF ingestion;
- meaningful document structure extraction;
- human review of automatically detected chapters;
- natural-sounding text-to-speech generation;
- chapter-level audio organization; and
- a usable, persistent web audio experience.

## 3. V1 User Journey

```text
User registers/logs in
        ↓
Uploads a PDF
        ↓
BookPilot creates a document/book record
        ↓
PDF is parsed
        ↓
Candidate chapters/sections are detected
        ↓
User reviews and edits the structure
        ↓
Text is normalized and chunked
        ↓
TTS generates chapter audio
        ↓
Audio chunks are assembled
        ↓
Chapter audio assets are stored
        ↓
User listens in the BookPilot player
        ↓
Playback position is persisted
```

## 4. Product Philosophy

### Free-first development

The local developer experience should not require paid infrastructure. External providers can be configured for higher-quality generation, but core application development must remain possible without a paid account.

### Review rather than false perfection

PDF parsing and chapter detection are inherently imperfect. V1 therefore treats structure detection as **candidate generation**, followed by a user review step. This is more practical than attempting to guarantee perfect chapter detection.

### Provider independence

Document parsing, storage, and TTS are abstracted so that a provider can be replaced later without rewriting the whole application.

### Bounded semester scope

The semester version prioritizes one reliable user journey over a long feature list.

## 5. V1 Scope

The first stable baseline includes:

- account registration and login;
- PDF upload and validation;
- document parsing;
- chapter/section detection;
- chapter review and editing;
- text normalization and chunking;
- asynchronous audiobook generation;
- chapter-level generated audio;
- personal library;
- book/chapter detail pages;
- persistent global audio player;
- progress persistence; and
- basic automated tests and documentation.

## 6. Explicit Non-Goals

The baseline does **not** attempt to become:

- a commercial audiobook marketplace;
- a subscription or payment product;
- a mobile application;
- a social reading platform;
- a recommendation engine;
- a full voice-acting platform;
- a voice-cloning system;
- a RAG chat product;
- a research-paper explainer platform; or
- an unlimited-storage service.

These may be considered later, but they must not destabilize V1.

## 7. Long-Term Direction

The audiobook generator is the first pipeline on top of a more general document platform.

A future architecture could reuse the same canonical document model and parsed representation for:

```text
              ┌───────────────┐
              │    Document   │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │     Parse     │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │    Structure  │
              └───────┬───────┘
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
       Audiobook             RAG
        Pipeline             Pipeline
             ↓                 ↓
       Chapter Audio     Document Q&A

             Future branches:
             • research explainers
             • summaries
             • alternate audio
             • document insights
```

## 8. Product Success Definition

For the semester baseline, success means a new developer can clone the repository, configure the documented local environment, start the application, create an account, upload a real PDF, review detected chapters, generate audio with the configured provider or development fallback, play the resulting audiobook, and see playback progress persist across navigation/reloads.
