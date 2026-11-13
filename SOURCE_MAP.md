# Source Map

This repository is a clean-room SourceLoop implementation. No pre-event project source, authored content, test fixture, screenshot, design template, or dependency tree was copied into it.

## Event-window source tree

| Source | Relationship |
| --- | --- |
| `sourceloop/data/campus_routes.json` | Original bilingual campus-routing micro-course authored during the event. |
| `sourceloop/graph.py` | Original deterministic Dijkstra trace implementation. |
| `sourceloop/content.py` | Original validation, public redaction, and literal note-import implementation. |
| `sourceloop/store.py` | Original SQLite persistence and review deduplication. |
| `sourceloop/app.py` | Original loopback HTTP application. |
| `sourceloop/export.py` | Original one-file offline export builder. |
| `sourceloop/static/` | Original browser interface, styling, and interaction code. |
| `tests/` | Original unit, integration, and browser acceptance tests. |
| `fixtures/import-demo.md` | Original demonstration notes authored for the import flow. |

## Pre-event project boundary

The pre-event CourseJesus/BUHACK workspace used for comparison was:

```text
F:\Hackathon-2026\CourseJesus-BUHACK
HEAD at audit: ad54c96297602359da1dc60089cb0847cb451e4e
Working tree at audit: clean
```

That workspace was inspected read-only. It was not used as a Git ancestor, source overlay, submodule, worktree, package, asset source, or runtime dependency for this entry.

## Why SourceLoop rather than a reused AccessBridge build

The verified event requirement prohibits submissions based on old projects. A code-compatible reuse of the pre-event AccessBridge implementation would not satisfy that requirement even if the repository itself were created new.

The team therefore made the scope explicit:

1. keep the learner problem;
2. remove all pre-event implementation and assets;
3. build a smaller complete product from an empty repository inside the event window;
4. record the difference rather than represent old work as new.

The result is a separate product identity, **SourceLoop**, with a new course, interface, API, database, tests, documentation, and Git history.

## Runtime and external services

- Python 3.11 standard library only at runtime.
- SQLite database local to the repository runtime directory.
- No cloud model, vector database, object store, analytics service, or production API.
- Browser tests use Playwright and its isolated Chromium build as development-only tools.

## Repository history

The public repository was created after the event opened. The first commit is:

```text
4fe0cbc  2026-11-13T10:00:51+08:00  docs: establish clean-room SourceLoop specification
```

See `HACKATHON_CHANGELOG.md` for the complete event-window change record.
