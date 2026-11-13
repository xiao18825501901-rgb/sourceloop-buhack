# Known Limitations

## Product scope

- One curated course is included: **Campus Routes Lab**. It demonstrates Dijkstra's shortest path and the non-negative-weight assumption.
- The proposed Stack and Lambert teaching modules are not included in this build.
- The app is a single-user local workspace. It has no accounts, roles, cloud sync, notifications, or multi-device state.
- Imported packs support Markdown/plain text only. PDF parsing and OCR are not implemented.
- A one-section import remains reading-only because the quote checks need another section to create a safe distractor.
- Imported material is capped at 150,000 characters and eight sections.
- No cloud model is used. Imported notes do not receive generated teaching explanations.
- The graph visual supports non-negative weighted graphs. It intentionally rejects negative weights.

## Assessment boundary

- The practice checks are demonstration checks, not an institution's official assessment.
- The app does not claim or measure improved grades.
- The exported HTML contains a fixed local answer key. It is a study aid, not a secure exam environment.
- Source links establish traceability inside the included pack; they do not establish external academic authority.

## Browser and platform

- Automated browser acceptance ran on Playwright's Chromium.
- Edge was also opened against the live app for a first visual smoke check and is represented by the captured desktop/mobile screenshots.
- Firefox and Safari were not run.
- The supported runtime target is Windows with Python 3.11 or newer.

## Deployment and access

- The server is intended for loopback use. It has no TLS, multi-tenant authorization, account recovery, or internet-facing hardening.
- The app does not provide a hosted public demo.
- Final MentorMates submission is not complete.
- YouTube upload is not complete because the available video account is not authenticated.
- Team eligibility is not complete: the 2–5 member rule is not satisfied by one confirmed person.
- Finalist attendance at HKBU requires a valid student card/HKID and an in-person attendee.

## Event and code provenance

- SourceLoop is a clean-room event project. It is not presented as a modification of, or build from, the pre-event CourseJesus project.
- The Git history records only the SourceLoop work performed after the event opened.
- No production CourseJesus service, database, credential, OSS bucket, Clerk user, Canvas token, EAS deployment, or release lock was used.
