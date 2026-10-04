# BookPilot Design Documentation

These documents define the current product and technical direction for BookPilot V1.

## Canonical Reading Order

Start here:

1. `00-idea-recap-and-vision.md` — what the product is and what V1 means.
2. `01-requirements.md` — what V1 must do.
3. `02-architecture.md` — how the application is organized.
4. `03-data-flow.md` — how a PDF becomes an audiobook.
5. `04-data-model.md` — persistent entities and relationships.
6. `05-pdf-parsing-and-chapter-chunking.md` — document pipeline details.
7. `06-tts-and-audio-pipeline.md` — audio-generation details.
8. `07-extensibility-and-plugin-model.md` — future-proofing boundaries.
9. `08-tech-stack.md` — technologies used/expected.
10. `09-saas-billing-security-legal.md` — SaaS/security/legal baseline.
11. `10-quality-and-testing.md` — quality bar and testing strategy.
12. `11-roadmap.md` — now/next/later scope.
13. `12-research-notes-and-sources.md` — technical sources and decisions.

## Source-of-Truth Rule

These documents are intended to be the canonical design reference for the current baseline. The implementation should agree with them.

When the repository evolves, update the relevant document rather than allowing architecture knowledge to exist only in conversations or individual developer memory.

## V1 Principle

> Build one reliable PDF-to-audiobook journey on a reusable document-processing foundation.

Avoid adding future features merely because the architecture supports them.
