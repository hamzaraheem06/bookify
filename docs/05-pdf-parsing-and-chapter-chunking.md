# BookPilot — PDF Parsing, Chapter Detection, and Chunking

## 1. Design Goal

The PDF pipeline should convert an uploaded document into a structured representation that downstream services can understand without depending on one PDF library's raw output.

## 2. Parser Abstraction

Use a `DocumentParser` interface with a normalized return type such as:

```text
DocumentParseResult
├── title
├── metadata
├── pages
├── blocks / paragraphs
├── headings
└── diagnostics
```

The primary implementation should use **Docling** when the final environment can install and run it reliably. Docling-specific objects must remain behind the adapter.

## 3. Parser Responsibilities

The parser should:

- read the source PDF;
- extract text;
- retain page association where practical;
- preserve structural information where available;
- identify headings/blocks where possible;
- expose diagnostics for failures or weak extraction.

It should not own TTS logic or frontend-specific concerns.

## 4. Chapter Detection

Chapter detection is heuristic.

Candidate signals may include:

- semantic heading information from the parser;
- explicit chapter labels;
- numbered headings;
- common section-heading patterns;
- structural changes between blocks;
- page boundaries;
- heading hierarchy where available.

The output should be a candidate list such as:

```text
1. Introduction
2. Foundations
3. Core Methods
4. Results
5. Conclusion
```

## 5. Confidence / Review Philosophy

The system should avoid pretending that every PDF can be perfectly understood automatically. Where confidence is low or structure is ambiguous, the book enters a review step instead of being silently converted into a poor audiobook.

The review interface is therefore a core product feature, not a workaround.

## 6. Normalization

Normalization should repair common extraction artifacts while preserving meaning.

Safe operations may include:

- whitespace normalization;
- joining line-break artifacts within paragraphs;
- removal of obvious repeated page markers when reliably detectable;
- removal of isolated page numbers when reliably detectable;
- cleanup of encoding/extraction noise;
- preserving paragraph boundaries when useful.

Aggressive rewriting or summarization is outside the normalization stage.

## 7. Chunking

TTS input should be represented as deterministic ordered chunks.

The chunker should:

- respect provider size limits;
- prefer sentence/paragraph boundaries;
- preserve sequence numbers;
- retain chapter association;
- generate stable ordering;
- avoid creating excessively tiny fragments;
- be independently testable.

Example:

```text
Chapter 4
  ├── Chunk 1
  ├── Chunk 2
  ├── Chunk 3
  └── Chunk 4
```

## 8. Failure Cases

The pipeline should explicitly handle:

- scanned/image-only PDFs;
- encrypted/password-protected PDFs when unsupported;
- malformed PDFs;
- empty or nearly empty extraction;
- books with no obvious chapter headings;
- books with unusual layouts;
- very large files.

V1 may reject unsupported documents with a clear message rather than trying to solve every document format.

## 9. Test Fixtures

Maintain small representative fixtures for:

- simple chaptered text PDF;
- numbered sections;
- noisy line breaks;
- a document with weak structure;
- an unsupported/problematic case where feasible.

The tests should verify normalized internal output rather than parser-library-specific raw objects.
