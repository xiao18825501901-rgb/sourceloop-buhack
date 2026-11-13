# Isolation Report

## Scope

SourceLoop runs as a separate application with its own source, Git metadata, Python process, port, database, exports, and browser test runtime.

```text
Application: F:\Hackathon-2026\BUHack-Cleanroom-20261113
Runtime:     F:\Hackathon-2026\BUHack-Cleanroom-20261113\runtime
Port:        127.0.0.1:8765
Test port:   127.0.0.1:8766
Database:    runtime/database/sourceloop.sqlite3
Test DB:     runtime/e2e/database/sourceloop.sqlite3
```

The app does not read environment variables for remote services. It contains no production database URL, object-store credential, identity-provider secret, model endpoint, or telemetry destination.

## Pre-event workspace check

At the audit on 2026-11-13:

```text
Path: F:\Hackathon-2026\CourseJesus-BUHACK
HEAD: ad54c96297602359da1dc60089cb0847cb451e4e
Branch: main
Status: clean
```

The final delivery check repeats this comparison before reporting final status. No reset, clean, checkout, migration, build, or service command was run against that workspace as part of SourceLoop.

The visual-quality candidate at `J:\CourseJesus\work\visual-quality-20261105\candidate` was also checked read-only. Its existing dirty working tree is outside SourceLoop’s write path and was not modified by this project.

## Data isolation

- SQLite only opens `runtime/database/sourceloop.sqlite3` by default.
- Imported packs, attempts, and review items stay inside that database.
- Export files go to `runtime/exports/`.
- Browser tests use `runtime/e2e/` and a dedicated port.
- `runtime/`, database files, Node modules, test reports, and environment files are Git-ignored.
- No real student records or course files were imported.

## Network and model isolation

- Server host defaults to `127.0.0.1`.
- No permissive CORS header is emitted.
- No cloud model or third-party API is called by the application.
- `Content-Security-Policy`, `Referrer-Policy`, `X-Content-Type-Options`, and `X-Frame-Options` are applied to app responses.
- The exported study pack embeds all CSS and JavaScript and makes no network request.
- The browser test sets the exported-file context offline and completes its controls and grading.

## Public repository exclusions

The repository excludes:

- `.env` and key-like files;
- runtime SQLite databases;
- test reports and trace archives;
- Node modules;
- local server logs;
- production configuration;
- private course material;
- student data.

## Reproducibility

Python runtime dependencies: none outside the standard library.

Browser test dependencies are recorded in `package.json` and `package-lock.json`. The Playwright Chromium build is development-only and is not committed.

A final secret/path scan and pre-event Git comparison are recorded in `ACCEPTANCE.json` and `TEST_RESULTS.md`.
