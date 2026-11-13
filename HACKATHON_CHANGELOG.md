# Event-Window Changelog

All times are HKT. The public Git history is authoritative; this file summarizes the product increments.

## 2026-11-13

### 10:00 — Clean-room foundation

Commit `4fe0cbc` — `docs: establish clean-room SourceLoop specification`

- Created the repository during the event window.
- Defined the product scope, API contract, security boundaries, and completion criteria.
- Recorded the no-reuse constraint and excluded pre-event source/assets.

### 10:02 — Deterministic graph core

Commit `1382cbd` — `feat: trace shortest paths deterministically`

- Added weighted-graph validation.
- Added a real Dijkstra trace with settlement, tentative-distance, relaxation, path, and unreachable states.
- Added tests for weighted cost, non-negative invariants, unreachable targets, and start/goal identity.

### 10:04 — Course and import core

Commit `6b37625` — `feat: add original bilingual course and safe note import`

- Added the original three-lesson bilingual course **Campus Routes Lab**.
- Added five exact source passages, nine objective checks, explanations, and source links.
- Added deterministic Markdown/plain-text import with literal quote and source-location checks.
- Added public-payload redaction so answers and explanations are not sent before submission.

### Morning build — Local application

- Added the loopback JSON HTTP server, request validation, 256 KiB body cap, security headers, and path-traversal guard.
- Added SQLite persistence for imports, attempts, and a deduplicated review queue.
- Added self-contained offline HTML export with escaped embedded data.
- Added a responsive bilingual study workspace with:
  - course and lesson navigation;
  - source desk;
  - live Dijkstra stepper;
  - server-graded practice and source-backed feedback;
  - review queue and manual resolution;
  - Markdown import dialog;
  - offline export;
  - larger text and reduced motion.
- Added Python unit/integration coverage and Playwright browser acceptance tests.
- Added real browser screenshots and an offline exported study pack under `evidence/`.

## Current verification state

The detailed latest result is in `TEST_RESULTS.md`. Product acceptance is tracked separately from external submission gates in `ACCEPTANCE.json`.

## Not claimed

- No final MentorMates submission.
- No uploaded public video.
- No team expansion.
- No production deployment.
- No measured learning outcome.
