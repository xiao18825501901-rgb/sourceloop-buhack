# Third-Party Licenses

## Runtime

SourceLoop's application runtime uses the Python 3.11 standard library. Python is distributed under the Python Software Foundation License. No third-party Python package is required to start or use the app.

The browser interface uses native HTML, CSS, JavaScript, and SVG. No web framework, icon package, web font, or remote asset is bundled.

## Development and acceptance

| Component | Use | License / terms |
| --- | --- | --- |
| Playwright | Browser automation and screenshots | Apache License 2.0 |
| Chrome for Testing / Chromium build installed by Playwright | Local automated browser | Google/Chromium terms; not redistributed in this repository |
| Node.js and npm | Development tooling | Node.js is MIT-licensed; npm is under its published terms |

`node_modules/`, downloaded browsers, and generated test reports are excluded from the repository.

## Content

The **Campus Routes Lab** text, questions, explanations, and source passages are original event-window content by the SourceLoop contributors. The demo Markdown fixture is also original.

The project does not include:

- third-party course text;
- textbook excerpts;
- screenshots of a previous project;
- stock photography;
- licensed media;
- model weights;
- student data.

## License of this repository

Original SourceLoop source and content are released under the MIT License in `LICENSE`.
