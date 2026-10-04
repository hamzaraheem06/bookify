# BookPilot — TTS and Audio Pipeline

## 1. Goal

Convert reviewed chapter text into reliable chapter-level audiobook audio while keeping the TTS implementation replaceable.

## 2. Provider Abstraction

Expose a stable internal interface such as:

```text
TTSProvider
    synthesize(text, configuration) -> AudioResult
```

The application should not know whether the implementation uses a cloud API, a local model, or a deterministic mock.

## 3. Provider Strategy

The architecture should support:

- ElevenLabs or another cloud provider for higher-quality production-like output;
- Qwen3-TTS or another local/self-hosted implementation where practical;
- a deterministic mock provider for automated tests and no-key development.

Provider choice belongs in configuration/infrastructure, not in core business logic.

## 4. Development Fallback

The application must remain usable for non-TTS development when no external API key exists.

A mock provider may generate deterministic test audio or use another clearly labeled development implementation. The UI and documentation must not imply that mock audio is production-quality speech.

## 5. Generation Sequence

```text
Approved chapter
      ↓
Normalize text
      ↓
Create ordered chunks
      ↓
For each chunk:
      TTS synthesis
      ↓
Validate audio result
      ↓
Store chunk result if needed
      ↓
Assemble chapter audio
      ↓
Measure/record duration
      ↓
Create AudioAsset
      ↓
Mark chapter complete
```

## 6. Chapter-Level Isolation

Each chapter should be independently processable. This prevents one provider failure from destroying an otherwise successful book generation.

## 7. Idempotency

Where practical, use a content fingerprint such as:

```text
hash(normalized_text + voice_config + relevant provider settings)
```

This can be used to detect reusable generated results and avoid unnecessary duplicate synthesis.

The exact cache strategy can remain simple in V1.

## 8. Retries

Retry transient provider/storage failures with bounded retry attempts. Permanent validation failures should not be retried indefinitely.

## 9. Audio Assembly

The assembler combines ordered chunk audio into one chapter asset where the chosen audio format permits reliable concatenation. Keep the assembly implementation behind a service so that the application is not coupled to one command-line/media tool.

If FFmpeg is used, document it as an explicit system dependency and provide a simple verification command.

## 10. Audio Validation

Before marking a chapter complete, validate that:

- the expected output file exists;
- its media type is plausible;
- it has a non-zero duration/size;
- it can be consumed by the browser player under the selected format.

## 11. Progress Tracking

Generation progress should be based on actual chapter/chunk work rather than a fake timer. The frontend should consume persisted state from the backend.

## 12. Future Improvements

Later versions may add:

- richer voice configuration;
- pronunciation dictionaries;
- dialogue/character handling;
- prosody controls;
- more expressive voice models;
- background music or mastering options.

These are outside the semester baseline.
