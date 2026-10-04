# BookPilot — SaaS, Billing, Security, and Legal Baseline

## 1. SaaS Positioning

BookPilot is designed as a SaaS-style application, but V1 is deliberately bounded.

The baseline should support future quotas and plans without requiring a billing system now.

Useful future metering dimensions include:

- number of uploaded books;
- storage consumed;
- generated audio duration;
- processing frequency.

## 2. Free-First Development

Local development should not require paid services. This does not imply that a hosted production SaaS can operate indefinitely without storage, compute, bandwidth, or third-party API costs.

## 3. Authentication

- Hash passwords using a modern password-hashing mechanism.
- Never store plaintext passwords.
- Keep secret keys in environment configuration.
- Set an explicit authentication/session strategy and use it consistently.

## 4. Authorization

Every private resource must be checked server-side.

Example principle:

```text
GET /books/{book_id}
        ↓
resolve authenticated user
        ↓
load book by id + owner
        ↓
allow only if owner matches
```

Do not rely on the frontend to hide another user's book.

## 5. File Security

Uploaded files should be:

- size-limited;
- validated as PDFs;
- stored using server-generated safe keys;
- kept outside executable/source directories where practical;
- associated with the authenticated user;
- deleted through controlled application paths.

Do not trust the original filename as a storage path.

## 6. Secrets

Never commit:

- TTS API keys;
- JWT/application secrets;
- database passwords;
- cloud credentials.

Use `.env.example` for documentation and `.env` for local secrets.

## 7. CORS and API Exposure

Development CORS may allow the local frontend origin. Production configuration should use an explicit allow-list rather than `*` for credentialed private applications.

## 8. Legal Boundaries

V1 is a user-provided-document transformation tool rather than a commercial audiobook catalog.

Users should only upload material they are legally entitled to process. The application should not include pirated books or imply that converting a copyrighted work automatically grants redistribution rights.

The project documentation should avoid making jurisdiction-specific legal conclusions. Any production legal policy should be reviewed appropriately before deployment.

## 9. Storage / Quotas

A practical hosted implementation should introduce bounded quotas to prevent accidental/uncontrolled resource consumption. Example controls include:

- maximum source PDF size;
- maximum active jobs;
- maximum generated audio storage;
- per-user rate limits.

Exact values belong in runtime configuration.

## 10. Future Billing

Payments are future scope. When introduced, billing should sit around existing usage boundaries rather than inside document parsing or TTS logic.

## 11. Privacy Principle

Book content can be sensitive or private. Avoid logging full document text unnecessarily. Access control and retention/deletion policies should be explicit in a hosted version.
