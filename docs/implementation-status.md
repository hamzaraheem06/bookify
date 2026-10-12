# BookPilot V1 implementation status

The 14 canonical design files described in the earlier ChatGPT conversation are already present under `docs/` (the README plus documents 00–12). The referenced conversation has no downloadable attachments in its available record, so there was no separate ZIP to import. Git history in this checkout contains only the initial commit; it cannot restore a different historical frontend. The current Discover, Library, book detail/review, upload, and global player UI have been preserved.

## Current status

| Area | Status | Evidence / remaining work |
| --- | --- | --- |
| Local setup | Running on SQLite fallback | Python 3.11, repo-local Node 24, project dependencies, API, worker, and Vite are running. Docker Desktop's engine still returns HTTP 500; PostgreSQL is unavailable. |
| Authentication | Implemented and browser-verified | Register/login, protected pages, and `/auth/me` work. Root validates a stored session and opens signed-in Home; expired sessions return to the public landing page. |
| Existing frontend | Preserved and browser-verified | Public landing, Discover, Search, Library, upload, chapter review, book details, and global player remain. Signed-in Home uses the existing design. Protected routes are registered directly so upload/library/book URLs resolve. |
| PDF ingestion and chapter review | Verified with a two-chapter PDF | Upload, background parse, detected chapter titles/content, editable review, and save-to-ready pass. Scanned PDFs still need OCR (out of scope). |
| Generation and playback | Verified with local demo clips | Worker generation, authenticated audio, stored/restored position, playback status/time, and auto-advance pass. Speed, volume, seek, and sleep controls are present. Mock mode plays bundled non-silent WAV fixtures offline; they do not narrate uploaded text. |
| Retry and cleanup | Implemented and API-tested | Failed jobs can be re-queued; completed chapters are skipped on generation retry. Book deletion removes stored source and chapter audio. |
| Authorization | Partially tested | Books/audio are owner-scoped. Automated tests cover progress history and cross-user progress; add explicit cross-user book/audio/delete cases. |
| Database | SQLite fallback active; Postgres pending | Alembic migrations run on the local SQLite database. Docker Desktop's Linux engine returned HTTP 500 even with local engine access; retry Postgres setup after WSL finishes installing/restarting. |
| Product scope | V1 only | Payments, marketplace/catalog, OCR, mobile clients, collaboration, and paid TTS are outside the documented baseline. |

## Step-by-step plan

1. Keep the current frontend as the product baseline. **Done:** fixed signed-in `/`, validated its session, repaired direct protected routes, made logout return to guest landing, and wired the existing mobile menu. **Remaining:** finish responsive/mobile visual QA.
2. Verify the acceptance path on SQLite. **Done:** register → upload text PDF → detect two chapters → save review → generate → play non-silent demo audio → restore progress → auto-advance, and change playback speed. **Remaining:** check volume/seek and user-facing failure states in the browser.
3. Add focused automated coverage for session handling, history, retry/idempotence, audio ownership, progress ownership, and deletion cleanup. **Done:** tests cover parser headings, retry, progress/history scoping, and source/audio deletion. **Remaining:** explicit cross-user book/audio/delete cases and end-to-end failure injection.
4. Recover Docker Desktop's WSL/Linux engine and start PostgreSQL from `docker-compose.yml`; apply migrations and rerun acceptance on PostgreSQL. **Blocked by the current Docker engine HTTP 500; WSL installation is still running.**
5. Review upload limits, malformed/scanned PDF behavior, failure messages, and file cleanup if a database transaction fails. Keep paid providers and credentials optional.
6. Update the README and this status document with verified PostgreSQL setup, limitations, and final QA results.

## Checks completed / pending

- [x] Backend tests: 7 passed (one dependency deprecation warning).
- [x] Frontend production build.
- [x] Browser check: login at `/` shows signed-in Home, and direct protected routes resolve.
- [x] Text PDF upload, chapter review/generation, non-silent demo WAV, progress restore, and chapter auto-advance.
- [x] API health and CORS check for `127.0.0.1:5173`.
- [ ] PostgreSQL health, migration, and acceptance pass after Docker's WSL engine becomes available.
- [x] Final diff whitespace/status review; removed the disposable QA account, uploaded PDFs, and generated audio.
