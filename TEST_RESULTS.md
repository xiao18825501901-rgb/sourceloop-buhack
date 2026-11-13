# Test Results

## Product acceptance

| Area | Status | Evidence |
| --- | --- | --- |
| Graph, content, import, store, HTTP API, and offline export | `TESTED_LOCAL` | `evidence/TEST_RESULTS_UNIT.txt` |
| Browser learning loop, grading, review, import, and export | `VERIFIED_BROWSER` | `evidence/TEST_RESULTS_PLAYWRIGHT.txt` |
| Offline HTML pack on `file://` with network disabled | `VERIFIED_BROWSER` | `evidence/ui-offline-file.png` |
| Desktop and mobile layouts | `VERIFIED_BROWSER` | `evidence/ui-desktop-1440.png`, `evidence/ui-mobile-390.png`, `evidence/ui-mobile-320.png` |
| Demo video capture from the live application | `TESTED_LOCAL` | `evidence/SourceLoop-demo.mp4` |
| GitHub publication and history | `VERIFIED_PLATFORM` after final push | `ACCEPTANCE.json` |
| MentorMates submission | `BLOCKED` | Requires authenticated team and final human confirmation |

## 2026-11-13 15:50 HKT — Python and integration

Command:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Result: **26/26 passed** in 0.854 seconds.

Coverage includes:

- deterministic weighted shortest paths, relaxation, unreachable goals, and non-negative validation;
- curated-content validation and public answer redaction;
- literal Markdown/plain-text import checks and rejection of oversized/unsafe input;
- SQLite attempts and source-linked deduplicated review behavior;
- HTTP security, request validation, path traversal, public pack, and export behavior;
- offline HTML structure, embedded JSON safety, and exported answer key.

The full readable output is saved at `evidence/TEST_RESULTS_UNIT.txt`.

The exported HTML was additionally inspected for `localhost`, `127.0.0.1`, private/production service URLs, and private workspace paths. The only HTTP namespace present is the standard SVG XML namespace; the exported study pack makes no network request.

## 2026-11-13 16:40 HKT — Browser acceptance

Command:

```powershell
npm run test:e2e
```

Result: **3/3 Playwright tests passed** in 32.8 seconds.

Coverage includes:

- desktop, 390px, and 320px layouts with no horizontal overflow;
- English/Chinese switching and larger-text/reduced-motion controls;
- all three lessons;
- a real Dijkstra trace ending at `LIB → CAN → LAB` with cost `9`;
- a wrong answer, source-backed feedback, and review creation;
- a correct retry that resolves the review item;
- local Markdown import;
- a downloaded offline export;
- opening that export with the browser context offline and completing practice locally;
- zero browser console or page errors.

The full readable output is saved at `evidence/TEST_RESULTS_PLAYWRIGHT.txt`. The interactive report is under `evidence/playwright-report/`.

## Release gates

`ACCEPTANCE.json` records the final release checks. It separates verified product work from external submission gates that require authenticated humans.
