# BookPilot — Roadmap

## NOW — Semester Baseline

Build and stabilize:

- authentication;
- PDF upload;
- document storage abstraction;
- PDF parsing;
- chapter detection;
- chapter review/editing;
- text normalization;
- deterministic chunking;
- background jobs;
- TTS provider abstraction;
- configurable production-quality provider;
- development/mock provider;
- chapter audio generation;
- personal library;
- book detail view;
- persistent global player;
- playback progress;
- ownership/security checks;
- migrations;
- tests;
- setup documentation.

## NEXT — Practical Improvements

Once V1 is stable, consider:

- better chapter-detection heuristics;
- improved PDF layout handling;
- better metadata extraction;
- richer TTS voice configuration;
- generation retry UI;
- better job progress visualization;
- storage quota enforcement;
- deployment automation;
- cloud object storage adapter;
- stronger end-to-end test coverage.

## LATER — Document Intelligence Platform

Potential larger features:

- RAG over uploaded documents;
- research-paper explanation pipeline;
- document summarization;
- alternate document-to-audio modes;
- pronunciation/custom dictionaries;
- richer dialogue handling;
- team/collaborative workspaces;
- subscriptions/billing;
- enterprise controls.

## Scope Rule

A proposed feature belongs in V1 only when it directly improves the core PDF-to-audiobook journey and can be implemented without weakening reliability or substantially increasing infrastructure complexity.
