# SourceLoop — Clean-Room MVP Specification

**Event:** BUHack 2.0, Tertiary Track, EdTech  
**Build window:** 2026-11-13 10:00 HKT through 2026-11-15 10:00 HKT  
**Repository policy:** This project starts from an empty repository created during the event. No code, copy, fixtures, tests, screenshots, or other authored assets from a pre-event project may be reused.

## Objective

SourceLoop is a local-first study workspace for university students. It turns course notes into a short learning loop:

1. Read an authored explanation attached to an exact source passage.
2. Explore a deterministic interactive model of the concept.
3. Answer objective retrieval checks graded by the local server.
4. Return missed concepts to a source-linked review queue.
5. Export the complete learning material as a self-contained offline HTML file.

The prototype must demonstrate a complete, judge-operable path rather than a static mockup. The included micro-course, **Campus Routes Lab**, teaches weighted graphs and Dijkstra's shortest-path algorithm. It is original content authored during the event.

The product's promise is deliberately narrow: **no cloud model, no invisible synthesis, and no unsourced answer key**. Authored lessons are curated; imported notes produce literal quote-retrieval checks rather than invented explanations.

## Assumptions

1. The primary target is a modern desktop browser, with an Edge-based automated test run and responsive checks down to 320 CSS pixels.
2. The app is a single-user local workspace. Accounts, cloud sync, and multi-tenant authorization are out of scope.
3. The runtime uses Python 3.11+ standard-library features and SQLite only. Node and Playwright are development/test dependencies.
4. Imported material is Markdown or plain text. PDF parsing, OCR, and external retrieval services are out of scope.
5. Built-in course content is bilingual English and Chinese. Imported notes retain their original language and are labelled accordingly.
6. Learning gains are not claimed; the verification target is product behavior and source traceability.
7. GitHub publication, video hosting, team eligibility, and final MentorMates submission are external gates.

## Commands

```powershell
cd F:\Hackathon-2026\BUHack-Cleanroom-20261113
python -m sourceloop --open
python -m unittest discover -s tests -p "test_*.py" -v
npm ci
npx playwright test
```

The supported startup command is:

```powershell
python -m sourceloop --host 127.0.0.1 --port 8765 --open
```

## Project Structure

```text
sourceloop/
  app.py             HTTP routing, request validation, startup
  content.py         course loading, validation, Markdown import
  export.py          self-contained offline HTML generation
  graph.py           deterministic weighted-graph trace
  store.py           SQLite attempts, review items, imported packs
  data/              original bilingual demo course
  static/            HTML, CSS, vanilla JS, favicon
tests/
  test_graph.py
  test_content.py
  test_api.py
  test_export.py
  e2e/               Playwright user journeys
fixtures/
  import-demo.md     original notes used to demonstrate local import
evidence/            runtime screenshots and result captures
docs/                public static showcase and supporting visuals
submission/          judging copy, demo script, checklist
runtime/             ignored local database, exports, and logs
```

## API Contract

- `GET /api/health` — process and database readiness.
- `GET /api/bootstrap` — pack summaries, default pack, review count.
- `GET /api/packs/{id}` — public pack payload without answers or explanations.
- `POST /api/attempts` — server-side grading for one lesson.
- `GET /api/review` — open source-linked review items.
- `POST /api/review/{id}/resolve` — mark a review item resolved.
- `POST /api/import` — parse Markdown/plain text into a local pack.
- `GET /api/export/{id}?lang=en|zh` — standalone offline study pack.

All mutations use `application/json`. Request bodies are capped at 256 KiB. The server is bound to loopback by default and does not add permissive CORS headers.

## Data Model

- Curated packs are validated JSON documents loaded from `sourceloop/data/`.
- Imported packs are serialized into SQLite with their original user title and timestamp.
- Attempts store scores and the submitted option identifiers.
- Review items store the lesson, concept, source code, prompt, and source quote so the queue remains understandable without a model.
- Runtime paths are independent of any pre-existing project database.

## Code Style

Use descriptive names, small functions, explicit error handling, and parameterized SQL. In the browser, insert external text through `textContent` or DOM nodes, never through `innerHTML`.

```python
def validate_option(question: dict, option_id: str) -> bool:
    return any(option["id"] == option_id for option in question["options"])
```

## Testing Strategy

- Unit tests: graph trace, content validation, import parsing, client payload redaction, source integrity.
- Integration tests: real loopback HTTP server, SQLite persistence, grading, review lifecycle, export.
- Browser tests: Playwright against Edge for navigation, bilingual UI, graph stepping, wrong-answer feedback, review queue, import, export download, offline file, mobile width, keyboard focus, and console errors.
- Security checks: request size, content type, path traversal, XSS-shaped import text, absent private URLs in export, secret scan.
- Evidence: exact command output, screenshot paths, exported-file path, and source repository state.

## Boundaries

### Always

- Keep runtime data under `runtime/`.
- Validate all HTML-bound external input through DOM text APIs.
- Use parameterized SQL.
- Run tests before each code-bearing commit.
- Preserve the pre-event repository untouched.

### Ask First

- Add a runtime dependency or external service.
- Change the data model in a way that discards existing local attempts.
- Publish the repository or upload a video before a final rights/secret check.

### Never

- Reuse pre-event source, content, screenshots, fixtures, or templates.
- Commit secrets or real student data.
- Make an external model call from the app.
- Claim verified learning impact, platform submission, or video publication without current evidence.

## Success Criteria

- A user can open the app, select a lesson, read both languages, expand source passages, step a real shortest-path computation, submit checks, and see source-backed feedback.
- A wrong answer creates exactly one deduplicated review item for that question; a correct retry resolves it.
- A Markdown file with at least two heading sections can become a local study pack with source cards and literal quote checks.
- The export downloads as one HTML file, opens through `file://`, works with the browser network context offline, and contains no private runtime URL.
- The UI has loading, error, empty, and retry states; keyboard focus is visible; 360/390/768/1024/1440px layouts avoid horizontal overflow.
- The repository contains reproducible setup, test instructions, limitations, and a clean-room source map.
- The public repository was created after 2026-11-13 10:00 HKT and contains meaningful event-window commits.

## External Gates

- A second confirmed human teammate is required by the 2–5 member rule. Inviting an unconfirmed contact or inventing a member is prohibited.
- YouTube upload requires an authenticated account.
- Final MentorMates submission requires a valid team and human confirmation at the submission action.
