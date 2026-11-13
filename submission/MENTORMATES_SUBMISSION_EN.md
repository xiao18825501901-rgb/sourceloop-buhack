# MentorMates Submission Copy — SourceLoop

## Project name

SourceLoop

## Tagline

Turn your notes into a cited, interactive study loop.

## Track and theme

- Track: Tertiary
- Theme: EdTech

## One-sentence description

SourceLoop is a local-first study workspace that links explanations, exact source passages, a real Dijkstra trace, server-graded checks, a source-backed review queue, and an offline study pack into one loop.

## Description

Students often lose the path from a wrong answer back to the exact course material they need to revisit. SourceLoop makes that path explicit.

The included **Campus Routes Lab** course teaches weighted graphs, Dijkstra’s algorithm, relaxation, and the non-negative-weight assumption in English and Chinese. Every taught point can be expanded to its exact source passage. The Dijkstra visual is driven by a real deterministic computation, not a prerecorded animation. Practice is graded by the local server; answers and explanations appear only after submission. A missed item becomes one deduplicated review entry tied to its source. A correct retry resolves it.

Students can also import their own Markdown or plain-text notes. The import creates literal quote and source-location checks rather than inventing explanations. Finally, the complete pack can be exported as one self-contained HTML file and used offline for reading, stepping, and practice.

## How to run

Requirements: Windows and Python 3.11 or newer.

```powershell
python -m sourceloop --host 127.0.0.1 --port 8765 --open
```

The app uses only the Python standard library and binds to `127.0.0.1`.

## Public repository

[github.com/xiao18825501901-rgb/sourceloop-buhack](https://github.com/xiao18825501901-rgb/sourceloop-buhack)

## Demo video

Local capture: `evidence/SourceLoop-demo.mp4`. Public URL: pending authenticated upload.

## Screenshots

- `evidence/ui-desktop-1440.png`
- `evidence/ui-graph-desktop.png`
- `evidence/ui-practice-feedback.png`
- `evidence/ui-mobile-390.png`
- `evidence/ui-offline-file.png`

## Verification

- 26/26 Python and integration tests passed.
- 3/3 browser acceptance tests passed.
- The downloaded offline pack was opened in an offline browser context and graded locally.
- Desktop and 390px/320px layouts were checked with no horizontal overflow.

## Provenance

The repository was created after the event opened. No pre-event implementation, course fixture, screenshot, template, or dependency tree was copied. `PRE_EVENT_BASELINE.md`, `SOURCE_MAP.md`, and `ISOLATION_REPORT.md` record this boundary.
