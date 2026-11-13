# Clean-Room Record

## Event basis

- Event: BUHack 2.0
- Theme: EdTech
- Track: Tertiary
- Window used: **2026-11-13 10:00 HKT through 2026-11-15 10:00 HKT**
- Official participant-facing submission system verified: MentorMates
- The Devpost listing is optional and is not treated as the judged submission path.

The rule basis was checked from the organizer page and organizer email available at build time. The implementation applies the stricter reading: no pre-event project reuse.

## Clean-room chronology

| Time (HKT) | Event |
| --- | --- |
| 2026-11-13 10:00 | Event build window opened. |
| 2026-11-13 10:00:12 | New repository metadata created. |
| 2026-11-13 10:00:51 | First clean-room specification commit `4fe0cbc`. |
| 2026-11-13 10:02:08 | Deterministic shortest-path trace committed as `1382cbd`. |
| 2026-11-13 10:04:44 | Original bilingual course and note import committed as `6b37625`. |
| 2026-11-13 morning | HTTP application, SQLite store, offline export, and browser workspace developed and tested. |

## Authorship and non-reuse statement

No pre-event repository source was copied. No pre-event course text, test fixture, screenshot, interface template, database, package lock, or generated artifact was copied. The named university locations in the course are ordinary examples, not institutional course material.

The included course text was authored for this event. The external references were limited to general programming concepts:

- weighted graphs;
- Dijkstra's algorithm;
- non-negative edge weights;
- Bellman-Ford as a contrast case.

The implementation uses no external code package at runtime. Development-only browser testing uses Playwright under its own license.

## Product renaming

The initial project concept used the name CourseJesus — AccessBridge. After applying the no-old-project rule, the implementation was narrowed and renamed to SourceLoop. The old name is not used as a claim of code lineage or as a submission asset.

## In-window evidence

The Git history in the public repository is the authoritative chronology. Acceptance artifacts record real command output, screenshots, an exported HTML file, and the tested source revision. Files that are generated locally or contain private runtime state are excluded from the public repository.

## Unverified or external items

The clean-room build itself does not establish:

- team eligibility;
- final MentorMates submission;
- video publication;
- judging outcome;
- finalist attendance;
- measured learning impact.

Those items are tracked in `ACCEPTANCE.json` and `KNOWN_LIMITATIONS.md`.
