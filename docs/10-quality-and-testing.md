# BookPilot — Quality and Testing

## 1. Quality Goal

The goal of the baseline is not exhaustive testing. It is a reliable, reproducible implementation of the main user journey with sensible protection against regressions.

## 2. Backend Test Layers

### Unit Tests

Test isolated logic such as:

- chapter detection;
- text normalization;
- chunking;
- status transitions;
- provider adapters using controlled mocks.

### Integration Tests

Test interactions among:

- FastAPI;
- authentication;
- database;
- file/storage adapter;
- job processing.

### API Tests

Verify request/response contracts and authorization behavior.

## 3. Required Security/Ownership Tests

At minimum:

- unauthenticated requests are rejected where required;
- a user can access their own book;
- one user cannot access another user's book;
- one user cannot retrieve another user's audio asset through an indirect ID;
- deletion does not allow cross-user resources.

## 4. Parser Tests

Use small deterministic PDF fixtures. Verify that the normalized parser output is correct enough for downstream chapter detection.

Do not make tests depend on exact internal classes from the parser library unless the adapter itself is being tested.

## 5. Chunker Tests

Verify:

- long text creates multiple chunks;
- sequence numbers are ordered;
- text is not lost;
- chunk output remains associated with the correct chapter.

## 6. TTS Tests

Use a mock provider for automated tests.

Test:

- provider interface behavior;
- error propagation;
- retry handling where implemented;
- chapter generation using deterministic fixtures.

Avoid using paid external TTS calls in ordinary CI tests.

## 7. Generation Tests

Verify that:

- queued jobs transition correctly;
- progress is updated;
- completed chapters remain completed after a later failure;
- retries do not duplicate successful work unnecessarily.

## 8. Playback Tests

At the data/API level, verify that playback position can be created, updated, read, and associated with the correct user/book/chapter.

Browser-level audio behavior should additionally be smoke-tested manually or through an end-to-end tool when practical.

## 9. Frontend Checks

At minimum:

- linting where configured;
- TypeScript/type checks where applicable;
- production build;
- smoke-test major routes;
- inspect browser console for major runtime errors.

## 10. Manual V1 QA Checklist

```text
[ ] Register
[ ] Login
[ ] Upload valid PDF
[ ] Reject invalid/non-PDF upload
[ ] Parse document
[ ] Display detected chapters
[ ] Edit chapter title/order/inclusion
[ ] Start generation
[ ] See meaningful progress
[ ] Generate chapter audio
[ ] Open completed book
[ ] Play audio
[ ] Seek
[ ] Change speed
[ ] Change chapter
[ ] Auto-advance
[ ] Navigate while player remains available
[ ] Refresh and restore progress
[ ] Logout
[ ] Verify another user cannot access the first user's book
[ ] Delete a book
```

## 11. Definition of Stable

A feature is considered baseline-stable when it:

1. works through its normal UI/API path;
2. has validation/error handling;
3. does not require manual database edits;
4. has at least focused automated coverage where it is logic-heavy;
5. is documented sufficiently for another team member to understand.
