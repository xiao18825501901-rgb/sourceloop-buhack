# SourceLoop — Optional Devpost Draft

> MentorMates is the official judging platform. This file is a ready-to-copy optional Devpost draft, not evidence of a Devpost submission.

## Project name

SourceLoop

## Tagline

Turn your notes into a cited, interactive study loop.

## Inspiration

Course material often explains an idea, but the return path from “I got this question wrong” back to the exact sentence that matters is easy to lose. SourceLoop treats that return path as the product: explanation, source, practice, feedback, review, and offline study are one loop.

## What it does

SourceLoop is a local-first study workspace. A learner can:

- read a bilingual three-lesson micro-course on weighted graphs and Dijkstra’s algorithm;
- switch between English and Chinese, use larger text, and reduce motion;
- expand the exact source passage behind an explanation;
- step a real Dijkstra trace through settlement, tentative distances, relaxations, and the final path;
- answer objective checks graded by the local server;
- receive answers, reasoning, and exact citations only after submission;
- see a missed concept enter a deduplicated review queue;
- resolve it by retrying successfully or explicitly resolving the item;
- import Markdown/plain-text notes and receive literal quote and source-location checks;
- export the complete pack as one offline HTML file that runs without a server.

## How we built it

- Python 3 standard library for the loopback HTTP server, deterministic shortest-path trace, SQLite storage, validation, grading, and one-file export.
- SQLite in a repository-local runtime directory for attempts, imports, and review items.
- Vanilla HTML, CSS, and JavaScript for a responsive accessible workspace.
- Playwright and Chromium for browser acceptance across desktop, 390px, and 320px layouts.
- No cloud model or third-party runtime service.

## Challenges we ran into

- The event rule ruled out reusing the pre-event implementation, so the team rebuilt a narrower product cleanly and documented the boundary.
- Making citations exact meant rejecting explanatory generation for imported notes and using literal retrieval checks instead.
- Keeping the graph trustworthy meant exposing the actual Dijkstra computation, not a prerecorded animation.
- Keeping the offline export useful meant embedding content, interaction, grading, and the computed trace while safely escaping data.

## Accomplishments

- A complete local learning loop from explanation to cited feedback to review.
- A real Dijkstra visual driven by computed state.
- A one-file offline study pack tested in an offline browser context.
- Browser and Python test evidence, including 1440/390/320px checks.

## What we learned

A study product becomes more reliable when it constrains its promise. Exact citations, deterministic visuals, and visible feedback are more useful to a learner than an unbounded generated answer.

## What's next

- Add more authored visual modules.
- Extend import formats beyond Markdown/plain text.
- Add optional accounts and sync.
- Test the loop with more students and measure retention without claiming unsupported outcomes.

## Built with

- Python
- SQLite
- HTML
- CSS
- JavaScript
- Playwright

## GitHub repository

[github.com/xiao18825501901-rgb/sourceloop-buhack](https://github.com/xiao18825501901-rgb/sourceloop-buhack)

## Demo instructions

Run:

```powershell
python -m sourceloop --host 127.0.0.1 --port 8765 --open
```

Then read a lesson, expand a source, step the graph, submit a wrong answer, review and retry it, import `fixtures/import-demo.md`, and export the offline pack.

## Screenshots

- `evidence/ui-desktop-1440.png`
- `evidence/ui-graph-desktop.png`
- `evidence/ui-practice-feedback.png`
- `evidence/ui-mobile-390.png`
- `evidence/ui-offline-file.png`

## Video link

Pending authenticated upload. The captured local artifact is `evidence/SourceLoop-demo.mp4`.
