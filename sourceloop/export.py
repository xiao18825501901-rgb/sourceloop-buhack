"""Build a self-contained offline study pack."""

from __future__ import annotations

import copy
import html
import json
from typing import Any

from sourceloop.graph import shortest_path_trace


def _safe_json(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        serialized.replace("<", "\\u003c")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def build_offline_export(pack: dict[str, Any], language: str) -> str:
    """Return one HTML file that can run from ``file://`` without a server."""

    export_pack = copy.deepcopy(pack)
    for lesson in export_pack["lessons"]:
        visual = lesson.get("visual")
        if visual is not None and visual.get("type") == "dijkstra":
            visual["trace"] = shortest_path_trace(
                visual,
                visual["start"],
                visual["goal"],
            )

    selected_language = language if language in {"en", "zh"} else "en"
    title = pack["title"][selected_language]
    subtitle = pack["subtitle"][selected_language]
    return (
        OFFLINE_TEMPLATE.replace("__LANG__", selected_language)
        .replace("__TITLE__", html.escape(title))
        .replace("__SUBTITLE__", html.escape(subtitle))
        .replace("__PACK_JSON__", _safe_json(export_pack))
    )


OFFLINE_TEMPLATE = r"""<!doctype html>
<html lang="__LANG__">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="A fixed, self-contained SourceLoop study pack.">
  <title>__TITLE__ · SourceLoop offline pack</title>
  <style>
    :root {
      --paper: #f3eee3;
      --paper-deep: #e7dece;
      --card: #fffaf0;
      --ink: #17231f;
      --muted: #5d6962;
      --teal: #0a6b60;
      --teal-dark: #064b45;
      --teal-wash: #d9ece5;
      --amber: #bb6c15;
      --amber-wash: #f8e6c7;
      --red: #a33a32;
      --red-wash: #f7dfda;
      --line: #c9c0b0;
      --shadow: 0 18px 50px rgba(39, 48, 43, .10);
      --radius: 18px;
      --serif: Georgia, "Times New Roman", "Noto Serif SC", serif;
      --sans: "Segoe UI", "Noto Sans SC", system-ui, sans-serif;
      --mono: "Cascadia Mono", "SFMono-Regular", Consolas, monospace;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 8% 8%, rgba(10, 107, 96, .10), transparent 26rem),
        linear-gradient(90deg, rgba(23, 35, 31, .035) 1px, transparent 1px),
        var(--paper);
      background-size: auto, 28px 28px, auto;
      font-family: var(--sans);
      line-height: 1.6;
    }
    button, input { font: inherit; }
    button { color: inherit; }
    a { color: var(--teal); }
    .skip-link {
      position: fixed;
      left: 1rem;
      top: -6rem;
      z-index: 100;
      padding: .7rem 1rem;
      color: white;
      background: var(--teal-dark);
      border-radius: 8px;
    }
    .skip-link:focus { top: 1rem; }
    .topbar {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem clamp(1rem, 4vw, 3.5rem);
      border-bottom: 1px solid var(--line);
      background: rgba(243, 238, 227, .93);
    }
    .brand {
      display: inline-flex;
      align-items: center;
      gap: .7rem;
      min-width: 0;
      font-weight: 800;
      letter-spacing: -.03em;
    }
    .brand-mark {
      display: grid;
      width: 2.1rem;
      height: 2.1rem;
      place-items: center;
      color: var(--card);
      background: var(--teal);
      border-radius: 50%;
      font-family: var(--serif);
      font-size: 1.25rem;
    }
    .top-context {
      min-width: 0;
      margin-left: auto;
      color: var(--muted);
      font-size: .86rem;
    }
    .lang-switch {
      min-width: 5.6rem;
      padding: .55rem .8rem;
      color: var(--teal-dark);
      background: transparent;
      border: 1px solid var(--teal);
      border-radius: 999px;
      cursor: pointer;
      font-weight: 750;
    }
    .lang-switch:hover { background: var(--teal-wash); }
    button:focus-visible, summary:focus-visible, input:focus-visible,
    label:has(input:focus-visible) {
      outline: 3px solid var(--amber);
      outline-offset: 3px;
    }
    .page {
      width: min(1240px, calc(100% - 2rem));
      margin: 0 auto;
      padding: clamp(1.2rem, 3vw, 2.8rem) 0 4rem;
    }
    .intro {
      max-width: 820px;
      margin-bottom: 1.7rem;
    }
    .eyebrow {
      margin: 0 0 .5rem;
      color: var(--teal);
      font-family: var(--mono);
      font-size: .78rem;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1, h2, h3, p { margin-top: 0; }
    h1 {
      margin-bottom: .65rem;
      font-family: var(--serif);
      font-size: clamp(2.2rem, 6vw, 4.6rem);
      font-weight: 500;
      letter-spacing: -.045em;
      line-height: .98;
    }
    .intro p:last-child {
      max-width: 66ch;
      margin-bottom: 0;
      color: var(--muted);
      font-size: clamp(1rem, 2vw, 1.17rem);
    }
    .layout {
      display: grid;
      grid-template-columns: 260px minmax(0, 1fr);
      gap: clamp(1.2rem, 3vw, 2.5rem);
      align-items: start;
    }
    .lesson-nav {
      position: sticky;
      top: 1rem;
      padding: .7rem;
      background: rgba(255, 250, 240, .72);
      border: 1px solid var(--line);
      border-radius: var(--radius);
    }
    .nav-label {
      padding: .65rem .7rem .4rem;
      color: var(--muted);
      font-family: var(--mono);
      font-size: .72rem;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .lesson-button {
      display: grid;
      grid-template-columns: 2rem minmax(0, 1fr);
      gap: .65rem;
      width: 100%;
      padding: .75rem;
      text-align: left;
      background: transparent;
      border: 0;
      border-radius: 12px;
      cursor: pointer;
    }
    .lesson-button:hover { background: var(--teal-wash); }
    .lesson-button[aria-current="page"] {
      color: var(--teal-dark);
      background: var(--teal-wash);
    }
    .lesson-number {
      color: var(--amber);
      font-family: var(--mono);
      font-size: .78rem;
      font-weight: 800;
    }
    .lesson-button strong { display: block; font-size: .9rem; line-height: 1.3; }
    .lesson-button small { color: var(--muted); }
    .lesson-card {
      overflow: hidden;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: calc(var(--radius) + 4px);
      box-shadow: var(--shadow);
    }
    .lesson-head {
      padding: clamp(1.3rem, 4vw, 2.8rem);
      border-bottom: 1px solid var(--line);
    }
    .lesson-meta {
      display: flex;
      flex-wrap: wrap;
      gap: .55rem 1rem;
      margin-bottom: 1rem;
      color: var(--muted);
      font-family: var(--mono);
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .lesson-head h2 {
      max-width: 18ch;
      margin-bottom: .7rem;
      font-family: var(--serif);
      font-size: clamp(2rem, 5vw, 3.8rem);
      font-weight: 500;
      letter-spacing: -.035em;
      line-height: 1.03;
    }
    .lesson-summary {
      max-width: 62ch;
      margin-bottom: 0;
      color: var(--muted);
      font-size: 1.08rem;
    }
    .reading {
      padding: clamp(1.3rem, 4vw, 2.8rem);
      border-bottom: 1px solid var(--line);
    }
    .reading-block { position: relative; max-width: 68ch; }
    .reading-block + .reading-block { margin-top: 1.5rem; }
    .reading-block.lead p {
      margin-bottom: .8rem;
      font-family: var(--serif);
      font-size: clamp(1.35rem, 3vw, 1.75rem);
      line-height: 1.3;
    }
    .reading-block p { margin-bottom: .8rem; }
    .callout {
      padding: 1.2rem 1.35rem;
      background: var(--amber-wash);
      border-left: 4px solid var(--amber);
      border-radius: 0 12px 12px 0;
    }
    .callout h3 { margin-bottom: .4rem; font-size: 1rem; }
    .callout p { margin-bottom: .7rem; }
    .source-chip {
      display: inline-flex;
      align-items: center;
      gap: .35rem;
      padding: .3rem .55rem;
      color: var(--teal-dark);
      background: var(--teal-wash);
      border: 0;
      border-radius: 999px;
      cursor: pointer;
      font-family: var(--mono);
      font-size: .72rem;
      font-weight: 700;
    }
    .source-chip:hover { text-decoration: underline; }
    .visual-section, .sources-section, .practice-section {
      padding: clamp(1.3rem, 4vw, 2.8rem);
      border-bottom: 1px solid var(--line);
    }
    .section-heading {
      display: flex;
      flex-wrap: wrap;
      align-items: end;
      justify-content: space-between;
      gap: .8rem;
      margin-bottom: 1.1rem;
    }
    .section-heading h3 {
      margin-bottom: .2rem;
      font-family: var(--serif);
      font-size: clamp(1.5rem, 3vw, 2.25rem);
      font-weight: 500;
      letter-spacing: -.025em;
    }
    .section-heading p { margin: 0; color: var(--muted); font-size: .9rem; }
    .visual-box {
      overflow: hidden;
      background: #fdf8ed;
      border: 1px solid var(--line);
      border-radius: 15px;
    }
    .graph-wrap { padding: .7rem; }
    #graph { display: block; width: 100%; height: auto; min-height: 220px; }
    .graph-edge { stroke: #9b968b; stroke-width: 3; }
    .graph-edge.final { stroke: var(--amber); stroke-width: 6; }
    .edge-label-bg { fill: var(--card); stroke: var(--line); stroke-width: 1; }
    .edge-label { fill: var(--ink); font: 700 13px var(--mono); }
    .node circle { fill: var(--card); stroke: #7d847e; stroke-width: 3; transition: 180ms ease; }
    .node.settled circle { fill: var(--teal-wash); stroke: var(--teal); }
    .node.current circle { fill: var(--amber); stroke: var(--amber); stroke-width: 5; }
    .node text { fill: var(--ink); font: 700 12px var(--sans); text-anchor: middle; pointer-events: none; }
    .node.current text { fill: #fffaf0; }
    .visual-controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: .55rem;
      padding: .85rem;
      border-top: 1px solid var(--line);
    }
    .control {
      padding: .55rem .85rem;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 9px;
      cursor: pointer;
      font-weight: 700;
    }
    .control.primary { color: white; background: var(--teal); border-color: var(--teal); }
    .control:disabled { cursor: not-allowed; opacity: .4; }
    .step-count { margin-left: auto; color: var(--muted); font: .78rem var(--mono); }
    .visual-output {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      border-top: 1px solid var(--line);
    }
    .distances { padding: 1rem; border-right: 1px solid var(--line); }
    .relaxations { padding: 1rem; }
    .micro-label {
      margin-bottom: .55rem;
      color: var(--muted);
      font: 700 .7rem var(--mono);
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    .distance-grid { display: flex; flex-wrap: wrap; gap: .35rem; }
    .distance-pill {
      padding: .3rem .5rem;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 7px;
      font: .75rem var(--mono);
    }
    .distance-pill.settled { background: var(--teal-wash); border-color: var(--teal); }
    .distance-pill.current { color: white; background: var(--teal); border-color: var(--teal); }
    .relaxation-line { margin: .25rem 0; font: .78rem var(--mono); }
    .muted { color: var(--muted); }
    .sources-grid { display: grid; gap: .65rem; }
    .source-card { background: #fdf8ed; border: 1px solid var(--line); border-radius: 12px; }
    .source-card summary {
      display: flex;
      align-items: center;
      gap: .7rem;
      padding: .9rem 1rem;
      cursor: pointer;
      list-style: none;
    }
    .source-card summary::-webkit-details-marker { display: none; }
    .source-card summary::after {
      content: "+";
      margin-left: auto;
      color: var(--teal);
      font: 700 1.3rem var(--mono);
    }
    .source-card[open] summary::after { content: "−"; }
    .source-code {
      flex: 0 0 auto;
      padding: .2rem .4rem;
      color: var(--teal-dark);
      background: var(--teal-wash);
      border-radius: 5px;
      font: 800 .72rem var(--mono);
    }
    .source-summary strong { display: block; font-size: .9rem; }
    .source-summary small { color: var(--muted); }
    .source-quote {
      margin: 0 1rem 1rem;
      padding: 1rem;
      color: #38433e;
      background: var(--card);
      border-left: 3px solid var(--teal);
      font-family: var(--serif);
      line-height: 1.7;
    }
    .practice-intro {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: .8rem;
      margin-bottom: 1rem;
    }
    .practice-intro p { max-width: 55ch; margin: 0; color: var(--muted); }
    .question-list { display: grid; gap: 1.4rem; }
    .question {
      padding: 1.1rem;
      background: #fdf8ed;
      border: 1px solid var(--line);
      border-radius: 14px;
    }
    .question fieldset { min-width: 0; padding: 0; margin: 0; border: 0; }
    .question legend {
      width: 100%;
      margin-bottom: .8rem;
      font-weight: 750;
      line-height: 1.45;
    }
    .question-number {
      display: inline-block;
      margin-right: .4rem;
      color: var(--amber);
      font-family: var(--mono);
      font-size: .78rem;
    }
    .option {
      display: flex;
      align-items: flex-start;
      gap: .65rem;
      padding: .7rem .8rem;
      border: 1px solid transparent;
      border-radius: 9px;
      cursor: pointer;
    }
    .option:hover { background: var(--teal-wash); }
    .option input { flex: 0 0 auto; margin-top: .3rem; accent-color: var(--teal); }
    .submit-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: .8rem;
      margin-top: 1.3rem;
    }
    .submit-button {
      padding: .75rem 1.15rem;
      color: white;
      background: var(--teal);
      border: 1px solid var(--teal);
      border-radius: 9px;
      cursor: pointer;
      font-weight: 750;
    }
    .submit-button:disabled { cursor: wait; opacity: .6; }
    .form-status { color: var(--red); font-size: .88rem; }
    .result-summary {
      margin-top: 1.2rem;
      padding: 1rem;
      background: var(--teal-wash);
      border: 1px solid var(--teal);
      border-radius: 12px;
    }
    .result-summary strong { font-family: var(--serif); font-size: 1.3rem; }
    .result-list { display: grid; gap: .8rem; margin-top: .8rem; }
    .result {
      padding: .85rem 1rem;
      background: var(--card);
      border-left: 4px solid var(--teal);
      border-radius: 0 9px 9px 0;
    }
    .result.incorrect { border-left-color: var(--red); }
    .result p { margin: .35rem 0; }
    .result .result-label { font-weight: 800; }
    .result.incorrect .result-label { color: var(--red); }
    .retry-button {
      margin-top: .7rem;
      padding: .5rem .75rem;
      background: transparent;
      border: 1px solid var(--teal);
      border-radius: 8px;
      cursor: pointer;
      font-weight: 700;
    }
    .empty-practice {
      padding: 1rem;
      color: var(--muted);
      background: var(--paper);
      border: 1px dashed var(--line);
      border-radius: 12px;
    }
    .lesson-footer {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 1rem;
      padding: 1.2rem clamp(1.3rem, 4vw, 2.8rem);
      color: var(--muted);
      font-size: .82rem;
    }
    .lesson-footer p { margin: 0; }
    .offline-seal {
      display: inline-flex;
      align-items: center;
      gap: .45rem;
      color: var(--teal-dark);
      font-family: var(--mono);
      font-size: .72rem;
      font-weight: 700;
      text-transform: uppercase;
    }
    .offline-seal::before {
      content: "";
      width: .55rem;
      height: .55rem;
      background: var(--teal);
      border-radius: 50%;
    }
    .export-note {
      max-width: 78ch;
      margin: 1rem auto 0;
      padding: 1rem 1.2rem;
      color: var(--muted);
      background: rgba(255, 250, 240, .65);
      border: 1px solid var(--line);
      border-radius: 12px;
      font-size: .84rem;
    }
    @media (max-width: 820px) {
      .top-context { display: none; }
      .layout { grid-template-columns: 1fr; }
      .lesson-nav {
        position: static;
        display: flex;
        gap: .35rem;
        overflow-x: auto;
        padding: .5rem;
      }
      .nav-label { display: none; }
      .lesson-button { flex: 0 0 185px; grid-template-columns: 1.5rem minmax(0, 1fr); }
      .visual-output { grid-template-columns: 1fr; }
      .distances { border-right: 0; border-bottom: 1px solid var(--line); }
    }
    @media (max-width: 520px) {
      .page { width: min(100% - 1rem, 1240px); padding-top: .8rem; }
      .topbar { padding: .75rem; }
      .brand { font-size: .9rem; }
      .lesson-card { border-radius: 14px; }
      .lesson-head, .reading, .visual-section, .sources-section, .practice-section {
        padding: 1.05rem;
      }
      .step-count { width: 100%; margin-left: 0; }
      .source-summary small { display: none; }
      .lesson-footer { padding: 1rem; }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      *, *::before, *::after { transition-duration: .01ms !important; animation-duration: .01ms !important; }
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#lesson-content">Skip to lesson</a>
  <header class="topbar">
    <div class="brand"><span class="brand-mark" aria-hidden="true">S</span><span>SourceLoop</span></div>
    <span class="top-context">__SUBTITLE__</span>
    <button class="lang-switch" id="lang-toggle" type="button">中文</button>
  </header>
  <main class="page">
    <div class="intro">
      <p class="eyebrow" id="offline-eyebrow">Offline study pack</p>
      <h1>__TITLE__</h1>
      <p id="pack-subtitle">__SUBTITLE__</p>
    </div>
    <div class="layout">
      <nav class="lesson-nav" id="lesson-nav" aria-label="Lessons"></nav>
      <article class="lesson-card" id="lesson-content" tabindex="-1">
        <header class="lesson-head">
          <div class="lesson-meta" id="lesson-meta"></div>
          <h2 id="lesson-title"></h2>
          <p class="lesson-summary" id="lesson-summary"></p>
        </header>
        <section class="reading" id="reading" aria-label="Lesson reading"></section>
        <section class="visual-section" id="visual-section" hidden>
          <div class="section-heading">
            <div>
              <h3 id="visual-title"></h3>
              <p id="visual-subtitle"></p>
            </div>
          </div>
          <div class="visual-box">
            <div class="graph-wrap">
              <svg id="graph" viewBox="0 0 648 432" role="img" aria-labelledby="graph-title"></svg>
            </div>
            <div class="visual-controls">
              <button class="control" id="reset-step" type="button"></button>
              <button class="control" id="back-step" type="button"></button>
              <button class="control primary" id="next-step" type="button"></button>
              <span class="step-count" id="step-count"></span>
            </div>
            <div class="visual-output">
              <div class="distances">
                <div class="micro-label" id="distances-label"></div>
                <div class="distance-grid" id="distance-grid"></div>
              </div>
              <div class="relaxations">
                <div class="micro-label" id="relaxations-label"></div>
                <div id="relaxation-log" aria-live="polite"></div>
              </div>
            </div>
          </div>
        </section>
        <section class="sources-section">
          <div class="section-heading">
            <div>
              <h3 id="sources-title"></h3>
              <p id="sources-subtitle"></p>
            </div>
          </div>
          <div class="sources-grid" id="source-list"></div>
        </section>
        <section class="practice-section">
          <div class="section-heading">
            <div>
              <h3 id="practice-title"></h3>
              <p id="practice-subtitle"></p>
            </div>
          </div>
          <div id="practice"></div>
        </section>
        <footer class="lesson-footer">
          <p id="footer-copy"></p>
          <span class="offline-seal" id="offline-seal"></span>
        </footer>
      </article>
    </div>
    <p class="export-note" id="export-note"></p>
  </main>
  <script id="pack-data" type="application/json">__PACK_JSON__</script>
  <script>
    "use strict";
    const pack = JSON.parse(document.getElementById("pack-data").textContent);
    const state = { lang: document.documentElement.lang === "zh" ? "zh" : "en", lesson: 0, step: 0 };
    const refs = {
      lang: document.getElementById("lang-toggle"),
      nav: document.getElementById("lesson-nav"),
      content: document.getElementById("lesson-content"),
      meta: document.getElementById("lesson-meta"),
      title: document.getElementById("lesson-title"),
      summary: document.getElementById("lesson-summary"),
      reading: document.getElementById("reading"),
      visualSection: document.getElementById("visual-section"),
      visualTitle: document.getElementById("visual-title"),
      visualSubtitle: document.getElementById("visual-subtitle"),
      graph: document.getElementById("graph"),
      stepCount: document.getElementById("step-count"),
      reset: document.getElementById("reset-step"),
      back: document.getElementById("back-step"),
      next: document.getElementById("next-step"),
      distances: document.getElementById("distance-grid"),
      distanceLabel: document.getElementById("distances-label"),
      relaxationLabel: document.getElementById("relaxations-label"),
      relaxations: document.getElementById("relaxation-log"),
      sources: document.getElementById("source-list"),
      practice: document.getElementById("practice"),
      eyebrow: document.getElementById("offline-eyebrow"),
      subtitle: document.getElementById("pack-subtitle"),
      sourcesTitle: document.getElementById("sources-title"),
      sourcesSubtitle: document.getElementById("sources-subtitle"),
      practiceTitle: document.getElementById("practice-title"),
      practiceSubtitle: document.getElementById("practice-subtitle"),
      footer: document.getElementById("footer-copy"),
      seal: document.getElementById("offline-seal"),
      note: document.getElementById("export-note")
    };
    const copy = {
      en: {
        langButton: "中文", lessonLabel: "Lesson", of: "of", minutes: "min", read: "Read",
        interactive: "Try the model", sourceNote: "Every claim above returns to one of these exact passages.",
        sourceTitle: "Source desk", sourcesSubtitle: "Open a source to inspect the exact wording.",
        practiceTitle: "Source-checked practice", practiceSubtitle: "Answers are graded inside this fixed file. Explanations stay tied to the source.",
        source: "Source", step: "Step", stepWord: "step", ofWord: "of", reset: "Reset", back: "Back", next: "Next step",
        settled: "Settled distances", relax: "Relaxations this step", noRelax: "No distance improved at this step.",
        finalPath: "Shortest path", unreachable: "No path reaches the goal.", start: "Start", goal: "Goal",
        submit: "Check answers", incomplete: "Choose one answer for every question.", attempt: "attempt",
        score: "You answered", correct: "correct", correctWord: "correct", incorrect: "Needs review",
        explanation: "Why", retry: "Try this lesson again", readingOnly: "This imported section is reading-only because it needs at least one other section for a safe comparison check.",
        offline: "Works offline", footer: "This is a fixed learning pack. It does not call a server, model, or account.",
        note: "Export note: these checks are validated locally by the embedded answer key. This file is a study aid, not the institution's official assessment.",
        visualTitles: { title: "Walk the frontier", subtitle: "The server computed this trace from the graph before export." }
      },
      zh: {
        langButton: "English", lessonLabel: "第", of: "课，共", minutes: "分钟", read: "阅读",
        interactive: "操作图解", sourceNote: "以上每个知识点都可以回到下面这些原文段落。",
        sourceTitle: "来源台", sourcesSubtitle: "展开来源，核对原始措辞。",
        practiceTitle: "来源校验练习", practiceSubtitle: "答案在这个固定文件内评分，解释始终与来源对应。",
        source: "来源", step: "步骤", stepWord: "步", ofWord: "共", reset: "重置", back: "上一步", next: "下一步",
        settled: "当前距离", relax: "本步松弛", noRelax: "这一步没有距离被改善。",
        finalPath: "最短路径", unreachable: "没有路径可以到达终点。", start: "起点", goal: "终点",
        submit: "核对答案", incomplete: "请为每道题选择一个答案。", attempt: "作答",
        score: "你答对了", correct: "题", correctWord: "正确", incorrect: "需要复习",
        explanation: "原因", retry: "重新练习本节", readingOnly: "这个导入章节只能阅读，因为至少需要另一个章节才能生成安全的比较检查。",
        offline: "离线可用", footer: "这是一份固定学习材料。不会调用服务器、模型或账号。",
        note: "导出说明：练习由文件内嵌答案在本地评分。此文件是学习辅助材料，不是学校的正式测评。",
        visualTitles: { title: "沿着边界走一遍", subtitle: "导出前，服务器已根据真实图计算了这条轨迹。" }
      }
    };
    const text = (value) => value && typeof value === "object" ? (value[state.lang] || value.en || "") : (value || "");
    const element = (tag, className, value) => {
      const node = document.createElement(tag);
      if (className) node.className = className;
      if (value !== undefined) node.textContent = String(value);
      return node;
    };
    const lessonSourceCodes = (lesson) => {
      const codes = new Set();
      for (const block of lesson.body || []) if (block.source) codes.add(block.source);
      for (const question of lesson.questions || []) if (question.source) codes.add(question.source);
      return codes;
    };
    function setStaticCopy() {
      const c = copy[state.lang];
      refs.lang.textContent = c.langButton;
      refs.eyebrow.textContent = state.lang === "zh" ? "离线学习包" : "Offline study pack";
      refs.sourcesTitle.textContent = c.sourceTitle;
      refs.sourcesSubtitle.textContent = c.sourcesSubtitle;
      refs.practiceTitle.textContent = c.practiceTitle;
      refs.practiceSubtitle.textContent = c.practiceSubtitle;
      refs.footer.textContent = c.footer;
      refs.seal.textContent = c.offline;
      refs.note.textContent = c.note;
      refs.subtitle.textContent = text(pack.subtitle);
      document.documentElement.lang = state.lang;
    }
    function renderNav() {
      const c = copy[state.lang];
      refs.nav.replaceChildren();
      const label = element("div", "nav-label", state.lang === "zh" ? "课程目录" : "Course map");
      refs.nav.append(label);
      pack.lessons.forEach((lesson, index) => {
        const button = element("button", "lesson-button");
        button.type = "button";
        button.setAttribute("aria-current", index === state.lesson ? "page" : "false");
        const number = element("span", "lesson-number", String(index + 1).padStart(2, "0"));
        const copyBox = element("span");
        copyBox.append(element("strong", "", text(lesson.title)), element("small", "", text(lesson.duration)));
        button.append(number, copyBox);
        button.addEventListener("click", () => {
          state.lesson = index;
          state.step = 0;
          render();
        });
        refs.nav.append(button);
      });
    }
    function sourceChip(code) {
      const c = copy[state.lang];
      const button = element("button", "source-chip", `${c.source} ${code}`);
      button.type = "button";
      button.setAttribute("aria-label", `${c.source} ${code}`);
      button.addEventListener("click", () => {
        const source = document.querySelector(`[data-source-card="${code}"]`);
        if (!source) return;
        source.open = true;
        source.scrollIntoView({ block: "center" });
        source.querySelector("summary").focus();
      });
      return button;
    }
    function renderReading(lesson) {
      refs.reading.replaceChildren();
      for (const block of lesson.body || []) {
        const wrapper = element("div", `reading-block ${block.kind}`);
        if (block.kind === "callout") {
          const callout = element("div", "callout");
          callout.append(element("h3", "", text(block.title)), element("p", "", text(block.text)));
          if (block.source) callout.append(sourceChip(block.source));
          wrapper.append(callout);
        } else {
          wrapper.append(element("p", "", text(block.text)));
          if (block.source) wrapper.append(sourceChip(block.source));
        }
        refs.reading.append(wrapper);
      }
      refs.reading.append(element("p", "muted", copy[state.lang].sourceNote));
    }
    function renderSources(lesson) {
      const c = copy[state.lang];
      refs.sources.replaceChildren();
      const codes = lessonSourceCodes(lesson);
      for (const source of pack.sources.filter((item) => codes.has(item.code))) {
        const details = element("details", "source-card");
        details.dataset.sourceCard = source.code;
        const summary = element("summary");
        const meta = element("span", "source-summary");
        meta.append(
          element("strong", "", text(source.title)),
          element("small", "", text(source.label))
        );
        summary.append(element("span", "source-code", source.code), meta);
        details.append(summary, element("blockquote", "source-quote", text(source.text)));
        refs.sources.append(details);
      }
      if (!refs.sources.children.length) {
        refs.sources.append(element("p", "muted", c.noSources || ""));
      }
    }
    function svgElement(tag, attributes) {
      const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
      for (const [name, value] of Object.entries(attributes || {})) node.setAttribute(name, String(value));
      return node;
    }
    function renderGraph(lesson) {
      const c = copy[state.lang];
      const visual = lesson.visual;
      refs.visualSection.hidden = !visual;
      if (!visual) return;
      refs.visualTitle.textContent = c.visualTitles.title;
      refs.visualSubtitle.textContent = c.visualTitles.subtitle;
      const trace = visual.trace;
      const currentStep = Math.min(state.step, trace.steps.length - 1);
      const step = trace.steps[currentStep];
      const final = currentStep === trace.steps.length - 1;
      const finalEdges = new Set();
      if (final && trace.path.length > 1) {
        for (let index = 0; index < trace.path.length - 1; index += 1) {
          finalEdges.add([trace.path[index], trace.path[index + 1]].sort().join("|"));
        }
      }
      refs.graph.replaceChildren();
      const graphTitle = svgElement("title", { id: "graph-title" });
      graphTitle.textContent = `${text(lesson.title)}: ${c.finalPath} ${trace.path.map((id) => {
        const node = visual.nodes.find((item) => item.id === id);
        return node ? text(node.label) : id;
      }).join(" → ")}`;
      refs.graph.append(graphTitle);
      const nodeMap = new Map(visual.nodes.map((node) => [node.id, node]));
      for (const edge of visual.edges) {
        const source = nodeMap.get(edge.from);
        const target = nodeMap.get(edge.to);
        if (!source || !target) continue;
        const key = [edge.from, edge.to].sort().join("|");
        const line = svgElement("line", {
          x1: source.x, y1: source.y, x2: target.x, y2: target.y,
          class: `graph-edge${finalEdges.has(key) ? " final" : ""}`
        });
        refs.graph.append(line);
        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;
        refs.graph.append(svgElement("rect", {
          x: midX - 14, y: midY - 12, width: 28, height: 24, rx: 6, class: "edge-label-bg"
        }));
        const weight = svgElement("text", {
          x: midX, y: midY + 5, "text-anchor": "middle", class: "edge-label"
        });
        weight.textContent = edge.weight;
        refs.graph.append(weight);
      }
      for (const node of visual.nodes) {
        const isCurrent = step.current === node.id;
        const isSettled = step.settled.includes(node.id);
        const group = svgElement("g", {
          class: `node${isCurrent ? " current" : isSettled ? " settled" : ""}`,
          transform: `translate(${node.x} ${node.y})`,
          "aria-label": `${text(node.label)}: ${step.distances[node.id] ?? copy[state.lang].unreachable}`
        });
        group.append(svgElement("circle", { r: 25 }));
        const label = svgElement("text", { y: 4 });
        label.textContent = node.id;
        group.append(label);
        refs.graph.append(group);
      }
      refs.stepCount.textContent = `${c.step} ${currentStep + 1} ${c.ofWord} ${trace.steps.length}`;
      refs.reset.textContent = c.reset;
      refs.back.textContent = c.back;
      refs.next.textContent = c.next;
      refs.back.disabled = currentStep === 0;
      refs.next.disabled = currentStep === trace.steps.length - 1;
      refs.reset.disabled = currentStep === 0;
      refs.distanceLabel.textContent = c.settled;
      refs.relaxationLabel.textContent = c.relax;
      refs.distances.replaceChildren();
      for (const node of visual.nodes) {
        const distance = step.distances[node.id];
        const pill = element("span", "distance-pill", `${node.id} ${distance === null ? "∞" : distance}`);
        if (step.current === node.id) pill.classList.add("current");
        else if (step.settled.includes(node.id)) pill.classList.add("settled");
        refs.distances.append(pill);
      }
      refs.relaxations.replaceChildren();
      if (!step.relaxations.length) {
        refs.relaxations.append(element("p", "relaxation-line muted", c.noRelax));
      } else {
        for (const relaxation of step.relaxations) {
          refs.relaxations.append(element(
            "p", "relaxation-line",
            `${relaxation.from}→${relaxation.to}: ${relaxation.previous === null ? "∞" : relaxation.previous} → ${relaxation.distance}`
          ));
        }
      }
      if (final) {
        const pathNames = trace.path.map((id) => text(nodeMap.get(id)?.label || id)).join(" → ");
        const summary = element("p", "relaxation-line final-summary", `${c.finalPath}: ${pathNames} · ${trace.distance ?? "∞"}`);
        refs.relaxations.append(summary);
      }
    }
    function renderPractice(lesson) {
      const c = copy[state.lang];
      refs.practice.replaceChildren();
      const questions = lesson.questions || [];
      if (!questions.length) {
        refs.practice.append(element("p", "empty-practice", c.readingOnly));
        return;
      }
      const intro = element("div", "practice-intro");
      intro.append(element("p", "", state.lang === "zh"
        ? `${questions.length} 道客观题。提交后会显示答案、解释与来源。`
        : `${questions.length} objective checks. Submit to reveal answers, reasoning, and the matching source.`));
      refs.practice.append(intro);
      const form = element("form", "question-list");
      form.noValidate = true;
      questions.forEach((question, index) => {
        const block = element("div", "question");
        const fieldset = element("fieldset");
        const legend = element("legend");
        legend.append(element("span", "question-number", String(index + 1).padStart(2, "0")), document.createTextNode(text(question.prompt)));
        fieldset.append(legend);
        question.options.forEach((option) => {
          const label = element("label", "option");
          const input = element("input");
          input.type = "radio";
          input.name = question.id;
          input.value = option.id;
          label.append(input, element("span", "", text(option.text)));
          fieldset.append(label);
        });
        block.append(fieldset);
        form.append(block);
      });
      const submitRow = element("div", "submit-row");
      const submit = element("button", "submit-button", c.submit);
      submit.type = "submit";
      const status = element("span", "form-status");
      status.setAttribute("role", "alert");
      submitRow.append(submit, status);
      form.append(submitRow);
      const results = element("div", "result-list");
      results.setAttribute("aria-live", "polite");
      refs.practice.append(form, results);
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        status.textContent = "";
        const data = new FormData(form);
        const answers = {};
        for (const question of questions) {
          const value = data.get(question.id);
          if (!value) {
            status.textContent = c.incomplete;
            const firstMissing = form.querySelector(`input[name="${question.id}"]`);
            if (firstMissing) firstMissing.focus();
            return;
          }
          answers[question.id] = String(value);
        }
        renderResults(lesson, answers, results);
        results.scrollIntoView({ block: "nearest" });
      });
    }
    function renderResults(lesson, answers, results) {
      const c = copy[state.lang];
      const sourceMap = new Map(pack.sources.map((source) => [source.code, source]));
      let score = 0;
      results.replaceChildren();
      const summary = element("div", "result-summary");
      for (const question of lesson.questions) if (answers[question.id] === question.answer) score += 1;
      summary.append(element("strong", "", `${c.score} ${score} / ${lesson.questions.length} ${c.correct}`));
      const retry = element("button", "retry-button", c.retry);
      retry.type = "button";
      retry.addEventListener("click", () => {
        results.replaceChildren();
        refs.practice.querySelectorAll("input[type=radio]").forEach((input) => { input.checked = false; });
        refs.practice.querySelector("input[type=radio]")?.focus();
      });
      summary.append(document.createElement("br"), retry);
      results.append(summary);
      for (const question of lesson.questions) {
        const isCorrect = answers[question.id] === question.answer;
        const result = element("div", `result${isCorrect ? "" : " incorrect"}`);
        result.append(element("p", "result-label", isCorrect ? `${c.correctWord} ✓` : `${c.incorrect} — ${c.explanation}`));
        result.append(element("p", "", text(question.explanation)));
        const source = sourceMap.get(question.source);
        if (source) {
          result.append(element("p", "muted", `${c.source} ${source.code} · ${text(source.title)}`));
        }
        results.append(result);
      }
    }
    function localLessonLabel(lesson, index) {
      const c = copy[state.lang];
      return state.lang === "zh"
        ? `${c.lessonLabel}${index + 1}${c.of}${pack.lessons.length}${c.minutes}`
        : `${c.lessonLabel} ${index + 1} ${c.of} ${pack.lessons.length}`;
    }
    function render() {
      setStaticCopy();
      renderNav();
      const lesson = pack.lessons[state.lesson];
      refs.meta.replaceChildren(
        element("span", "", text(lesson.kicker)),
        element("span", "", localLessonLabel(lesson, state.lesson)),
        element("span", "", text(lesson.duration))
      );
      refs.title.textContent = text(lesson.title);
      refs.summary.textContent = text(lesson.summary);
      renderReading(lesson);
      renderGraph(lesson);
      renderSources(lesson);
      renderPractice(lesson);
      document.title = `${text(lesson.title)} · ${text(pack.title)}`;
      refs.content.focus({ preventScroll: true });
    }
    refs.lang.addEventListener("click", () => {
      state.lang = state.lang === "en" ? "zh" : "en";
      render();
    });
    refs.reset.addEventListener("click", () => { state.step = 0; renderGraph(pack.lessons[state.lesson]); });
    refs.back.addEventListener("click", () => {
      state.step = Math.max(0, state.step - 1);
      renderGraph(pack.lessons[state.lesson]);
    });
    refs.next.addEventListener("click", () => {
      const trace = pack.lessons[state.lesson].visual.trace;
      state.step = Math.min(trace.steps.length - 1, state.step + 1);
      renderGraph(pack.lessons[state.lesson]);
    });
    render();
  </script>
</body>
</html>
"""
