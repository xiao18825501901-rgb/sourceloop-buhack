"use strict";

const STORAGE = {
  language: "sourceloop.language",
  pack: "sourceloop.pack",
  lesson: "sourceloop.lesson",
  largeText: "sourceloop.largeText",
  reduceMotion: "sourceloop.reduceMotion"
};

const copy = {
  en: {
    htmlLang: "en",
    languageButton: "中文",
    languageAria: "切换到中文",
    largerText: "Larger text",
    largerTextOn: "Standard text",
    largerTextAria: "Use larger text",
    largerTextOffAria: "Use standard text size",
    reduceMotion: "Reduce motion",
    reduceMotionOn: "Motion reduced",
    reduceMotionAria: "Reduce motion",
    reduceMotionOffAria: "Restore normal motion",
    export: "Export offline",
    exporting: "Preparing…",
    privacy: "Private workspace",
    noModel: "No cloud model",
    studyPack: "Study pack",
    courseMap: "Course map",
    currentPack: "Choose a study pack",
    bringNotes: "Bring your own notes",
    bringNotesSub: "Markdown or text · stays local",
    reviewQueue: "Review queue",
    reviewIntro: "Missed checks land here with the exact source you need.",
    openReviewAria: "Open review items",
    noLoops: "No open loops",
    noLoopsBody: "Miss a check and it will return here with its source.",
    methodRead: "Read. Every taught idea points back to an exact passage.",
    methodTest: "Test. The local server grades objective checks.",
    methodReturn: "Return. A missed check becomes one source-linked review item.",
    importAnother: "Import another note pack",
    importEyebrow: "Local import",
    importTitle: "Turn your notes into a study loop.",
    importIntro: "SourceLoop keeps your text as the source of truth. It creates literal quote and source-location checks rather than inventing explanations.",
    importPackTitle: "Pack title",
    importPackPlaceholder: "e.g. Memory & Retrieval",
    chooseFile: "Choose a .md or .txt file",
    orPaste: "Or paste your notes",
    importPlaceholder: "# First section\n\nPaste at least two headed sections…",
    importHelp: "Use two or more Markdown headings for quote checks.",
    importCancel: "Cancel",
    importBuild: "Build local study pack",
    importBuilding: "Building study loop…",
    importEmpty: "Paste your notes or choose a text file first.",
    importUnreadable: "That file could not be read as text.",
    closeImport: "Close import dialog",
    source: "Source",
    sourceTitle: "Source desk",
    sourceSubtitle: "Every taught idea has a return path. Open a passage to inspect the exact wording.",
    sourceOpen: "Open source",
    checks: "checks",
    sourceOne: "source",
    sourceMany: "sources",
    lessonOf: "of",
    minute: "min",
    authored: "Authored micro-course",
    importedTag: "Your local notes",
    readingNote: "The explanation is authored for this demo. The linked passage remains the source of truth.",
    interactiveTitle: "Walk the frontier",
    interactiveSubtitle: "A real Dijkstra trace computed by the local server, not a prerecorded animation.",
    start: "Start",
    goal: "Goal",
    step: "Step",
    reset: "Reset",
    back: "Back",
    next: "Next step",
    distances: "Tentative distances",
    relaxations: "Relaxed this step",
    noRelax: "No distance improved.",
    path: "Shortest path",
    cost: "cost",
    unreachable: "No path reaches the goal.",
    current: "Current node",
    practiceTitle: "Practice the return path",
    practiceSubtitle: "Answer from memory, then inspect the reasoning and the exact passage behind it.",
    practiceType: "Objective · server-graded",
    practiceIntroOne: "objective check",
    practiceIntroMany: "objective checks",
    practiceIntroEnd: "Submit once to grade the whole lesson.",
    submit: "Check answers",
    checking: "Checking…",
    incomplete: "Choose one answer for every question.",
    correct: "Correct",
    incorrect: "Needs review",
    correctAnswer: "Correct answer",
    yourAnswer: "Your answer",
    answerMatched: "Your answer matched.",
    explanation: "Why this is true",
    sourceBack: "Open source",
    score: "You answered",
    scoreEnd: "correctly.",
    wrongAddedOne: "One missed concept was added to the review queue.",
    wrongAddedMany: "missed concepts were added to the review queue.",
    noWrong: "Nothing was added to review. Your queue is clear.",
    tryAgain: "Try this lesson again",
    reviewUpdated: "Review queue updated.",
    noPractice: "This imported section is reading-only because it needs at least one other section for a safe comparison check.",
    previous: "Previous lesson",
    nextLesson: "Next lesson",
    studied: "studied",
    best: "best",
    reviewOpen: "Open lesson",
    reviewDone: "Mark reviewed",
    reviewAttempt: "attempt",
    reviewAttempts: "attempts",
    reviewResolved: "Review item resolved.",
    reviewReview: "Open the exact lesson",
    importSuccess: "Local study pack created.",
    exportSuccess: "Offline study pack downloaded.",
    exportFailure: "The offline pack could not be generated.",
    loading: "Reading your study pack…",
    loadFailure: "The local workspace could not be loaded.",
    packFailure: "That study pack could not be opened.",
    retry: "Try again",
    errorPrefix: "Local error:"
  },
  zh: {
    htmlLang: "zh",
    languageButton: "English",
    languageAria: "Switch to English",
    largerText: "大字模式",
    largerTextOn: "标准字号",
    largerTextAria: "开启大字模式",
    largerTextOffAria: "恢复标准字号",
    reduceMotion: "减少动效",
    reduceMotionOn: "动效已减少",
    reduceMotionAria: "减少动效",
    reduceMotionOffAria: "恢复正常动效",
    export: "导出离线包",
    exporting: "正在生成…",
    privacy: "本地私有空间",
    noModel: "不调用云端模型",
    studyPack: "学习包",
    courseMap: "课程地图",
    currentPack: "选择学习包",
    bringNotes: "导入自己的笔记",
    bringNotesSub: "Markdown 或纯文本 · 仅存本地",
    reviewQueue: "复习队列",
    reviewIntro: "答错的知识点会连同对应原文回到这里。",
    openReviewAria: "打开复习项目数量",
    noLoops: "没有待复习项",
    noLoopsBody: "答错一道检查题后，它会带着来源回到这里。",
    methodRead: "阅读。每个知识点都回到一段准确原文。",
    methodTest: "练习。客观题由本地服务器评分。",
    methodReturn: "返回。错题成为一个来源明确的复习项。",
    importAnother: "导入另一份笔记",
    importEyebrow: "本地导入",
    importTitle: "把笔记变成一个学习闭环。",
    importIntro: "SourceLoop 把你的文本作为唯一事实来源。它生成字面引文与来源定位题，不会凭空发明解释。",
    importPackTitle: "学习包标题",
    importPackPlaceholder: "例如：记忆与提取",
    chooseFile: "选择 .md 或 .txt 文件",
    orPaste: "或粘贴笔记",
    importPlaceholder: "# 第一节\n\n粘贴至少两个带标题的章节……",
    importHelp: "使用两个以上 Markdown 标题，才能生成引文检查。",
    importCancel: "取消",
    importBuild: "生成本地学习包",
    importBuilding: "正在生成学习闭环…",
    importEmpty: "请先粘贴笔记或选择文本文件。",
    importUnreadable: "无法以文本方式读取该文件。",
    closeImport: "关闭导入窗口",
    source: "来源",
    sourceTitle: "来源台",
    sourceSubtitle: "每个知识点都有返回路径。展开段落，核对原始措辞。",
    sourceOpen: "展开来源",
    checks: "道检查",
    sourceOne: "个来源",
    sourceMany: "个来源",
    lessonOf: "共",
    minute: "分钟",
    authored: "原创微课",
    importedTag: "你的本地笔记",
    readingNote: "讲解为演示课程所写；对应的原文段落仍然是事实基准。",
    interactiveTitle: "沿着边界走一遍",
    interactiveSubtitle: "轨迹由本地服务器真实计算，不是预制动画。",
    start: "起点",
    goal: "终点",
    step: "步骤",
    reset: "重置",
    back: "上一步",
    next: "下一步",
    distances: "暂定距离",
    relaxations: "本步松弛",
    noRelax: "没有距离被改善。",
    path: "最短路径",
    cost: "成本",
    unreachable: "没有路径可以到达终点。",
    current: "当前节点",
    practiceTitle: "练习返回来源",
    practiceSubtitle: "先凭记忆作答，再检查解释和支撑它的准确原文。",
    practiceType: "客观题 · 本地服务器评分",
    practiceIntroOne: "道客观检查",
    practiceIntroMany: "道客观检查",
    practiceIntroEnd: "一次提交，完成整节评分。",
    submit: "核对答案",
    checking: "正在评分…",
    incomplete: "请为每道题选择一个答案。",
    correct: "正确",
    incorrect: "需要复习",
    correctAnswer: "正确答案",
    yourAnswer: "你的答案",
    answerMatched: "你的答案一致。",
    explanation: "为什么",
    sourceBack: "展开来源",
    score: "本节答对",
    scoreEnd: "题。",
    wrongAddedOne: "一个未掌握概念已加入复习队列。",
    wrongAddedMany: "个未掌握概念已加入复习队列。",
    noWrong: "没有新增复习项，队列保持清空。",
    tryAgain: "重新练习本节",
    reviewUpdated: "复习队列已更新。",
    noPractice: "这个导入章节只能阅读，因为至少需要另一个章节才能生成安全的比较检查。",
    previous: "上一课",
    nextLesson: "下一课",
    studied: "已学习",
    best: "最高",
    reviewOpen: "打开课程",
    reviewDone: "标记已复习",
    reviewAttempt: "次作答",
    reviewAttempts: "次作答",
    reviewResolved: "复习项已解决。",
    reviewReview: "回到准确课程",
    importSuccess: "本地学习包已生成。",
    exportSuccess: "离线学习包已下载。",
    exportFailure: "无法生成离线学习包。",
    loading: "正在读取学习包…",
    loadFailure: "本地学习空间无法加载。",
    packFailure: "无法打开这个学习包。",
    retry: "重试",
    errorPrefix: "本地错误："
  }
};

class ApiFailure extends Error {
  constructor(message, code = "REQUEST_FAILED", retryable = false) {
    super(message);
    this.name = "ApiFailure";
    this.code = code;
    this.retryable = retryable;
  }
}

const state = {
  lang: readStorage(STORAGE.language) === "zh" ? "zh" : "en",
  largeText: readStorage(STORAGE.largeText) === "true",
  reduceMotion: readStorage(STORAGE.reduceMotion) === "true",
  bootstrap: null,
  pack: null,
  lessonIndex: 0,
  step: 0,
  reviewItems: [],
  submitBusy: false,
  visualSection: null,
  toastTimer: null
};

const refs = {
  html: document.documentElement,
  loading: document.getElementById("loading-screen"),
  errorScreen: document.getElementById("error-screen"),
  errorMessage: document.getElementById("error-message"),
  retryLoad: document.getElementById("retry-load"),
  shell: document.getElementById("app-shell"),
  langButton: document.getElementById("lang-button"),
  langLabel: document.getElementById("lang-label"),
  textButton: document.getElementById("text-button"),
  motionButton: document.getElementById("motion-button"),
  exportButton: document.getElementById("export-button"),
  importOpen: document.getElementById("import-open"),
  importCard: document.getElementById("import-card"),
  reviewImport: document.getElementById("review-import"),
  packSelect: document.getElementById("pack-select"),
  lessonList: document.getElementById("lesson-list"),
  courseProgress: document.getElementById("course-progress"),
  lessonView: document.getElementById("lesson-view"),
  mainContent: document.getElementById("main-content"),
  reviewCount: document.getElementById("review-count"),
  reviewList: document.getElementById("review-list"),
  reviewEmpty: document.getElementById("review-empty"),
  reviewHeading: document.getElementById("review-heading"),
  reviewIntro: document.getElementById("review-intro"),
  reviewEmptyTitle: document.getElementById("review-empty-title"),
  reviewEmptyBody: document.getElementById("review-empty-body"),
  privacy: document.getElementById("privacy-label"),
  noModel: document.getElementById("no-model-label"),
  packLabel: document.getElementById("pack-label"),
  courseMapLabel: document.getElementById("course-map-label"),
  importCardTitle: document.getElementById("import-card-title"),
  importCardSubtitle: document.getElementById("import-card-subtitle"),
  methodRead: document.getElementById("method-read"),
  methodTest: document.getElementById("method-test"),
  methodReturn: document.getElementById("method-return"),
  dialog: document.getElementById("import-dialog"),
  importForm: document.getElementById("import-form"),
  importHeading: document.getElementById("import-heading"),
  importEyebrow: document.getElementById("import-eyebrow"),
  importIntro: document.getElementById("import-intro"),
  importTitle: document.getElementById("import-title"),
  importFile: document.getElementById("import-file"),
  importText: document.getElementById("import-text"),
  importSize: document.getElementById("import-size"),
  importStatus: document.getElementById("import-status"),
  importSubmit: document.getElementById("import-submit"),
  importCancel: document.getElementById("import-cancel"),
  importClose: document.getElementById("import-close"),
  importTitleLabel: document.getElementById("import-title-label"),
  importFileLabel: document.getElementById("import-file-label"),
  importTextLabel: document.getElementById("import-text-label"),
  importHelp: document.getElementById("import-help"),
  toast: document.getElementById("toast")
};

function readStorage(key) {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function writeStorage(key, value) {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // The app remains usable when file or browser policy blocks storage.
  }
}

function ui(key) {
  return copy[state.lang][key];
}

function localized(value) {
  if (value && typeof value === "object") {
    return value[state.lang] || value.en || value.zh || "";
  }
  return value || "";
}

function node(tag, className = "", text = null) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== null && text !== undefined) element.textContent = String(text);
  return element;
}

function append(parent, ...children) {
  for (const child of children) {
    if (child !== null && child !== undefined) parent.append(child);
  }
  return parent;
}

function svgNode(tag, attributes = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [name, value] of Object.entries(attributes)) {
    element.setAttribute(name, String(value));
  }
  return element;
}

function currentLesson() {
  return state.pack?.lessons[state.lessonIndex] || null;
}

function currentLessonRows() {
  return currentLesson()?.questions || [];
}

async function api(path, options = {}) {
  const request = {
    method: options.method || "GET",
    headers: { Accept: "application/json" },
    signal: options.signal
  };
  if (options.body !== undefined) {
    request.headers["Content-Type"] = "application/json";
    request.body = JSON.stringify(options.body);
  }
  let response;
  try {
    response = await fetch(path, request);
  } catch {
    throw new ApiFailure(ui("loadFailure"), "NETWORK_UNAVAILABLE", true);
  }
  const contentType = response.headers.get("Content-Type") || "";
  let payload = null;
  if (contentType.includes("application/json")) {
    try {
      payload = await response.json();
    } catch {
      payload = null;
    }
  }
  if (!response.ok) {
    const error = payload?.error;
    throw new ApiFailure(
      error?.message || ui("loadFailure"),
      error?.code || "HTTP_ERROR",
      Boolean(error?.retryable)
    );
  }
  return payload;
}

function applyPreferences() {
  refs.html.lang = state.lang;
  refs.html.dataset.textSize = state.largeText ? "large" : "normal";
  refs.html.dataset.reducedMotion = String(state.reduceMotion);
  refs.textButton.setAttribute("aria-pressed", String(state.largeText));
  refs.motionButton.setAttribute("aria-pressed", String(state.reduceMotion));
  refs.textButton.setAttribute(
    "aria-label",
    state.largeText ? ui("largerTextOffAria") : ui("largerTextAria")
  );
  refs.motionButton.setAttribute(
    "aria-label",
    state.reduceMotion ? ui("reduceMotionOffAria") : ui("reduceMotionAria")
  );
  refs.langLabel.textContent = ui("languageButton");
  refs.langButton.setAttribute("aria-label", ui("languageAria"));
}

function renderStaticCopy() {
  applyPreferences();
  refs.privacy.textContent = ui("privacy");
  refs.noModel.textContent = ui("noModel");
  refs.packLabel.textContent = ui("studyPack");
  refs.courseMapLabel.textContent = ui("courseMap");
  refs.packSelect.setAttribute("aria-label", ui("currentPack"));
  refs.importCardTitle.textContent = ui("bringNotes");
  refs.importCardSubtitle.textContent = ui("bringNotesSub");
  refs.reviewHeading.textContent = ui("reviewQueue");
  refs.reviewIntro.textContent = ui("reviewIntro");
  refs.reviewCount.setAttribute("aria-label", ui("openReviewAria"));
  refs.reviewEmptyTitle.textContent = ui("noLoops");
  refs.reviewEmptyBody.textContent = ui("noLoopsBody");
  refs.methodRead.textContent = ui("methodRead");
  refs.methodTest.textContent = ui("methodTest");
  refs.methodReturn.textContent = ui("methodReturn");
  refs.reviewImport.textContent = ui("importAnother");
  refs.importEyebrow.textContent = ui("importEyebrow");
  refs.importHeading.textContent = ui("importTitle");
  refs.importIntro.textContent = ui("importIntro");
  refs.importTitleLabel.textContent = ui("importPackTitle");
  refs.importTitle.placeholder = ui("importPackPlaceholder");
  refs.importFileLabel.textContent = ui("chooseFile");
  refs.importTextLabel.textContent = ui("orPaste");
  refs.importText.placeholder = ui("importPlaceholder");
  refs.importHelp.textContent = ui("importHelp");
  refs.importCancel.textContent = ui("importCancel");
  refs.importSubmit.textContent = ui("importBuild");
  refs.importClose.setAttribute("aria-label", ui("closeImport"));
  refs.textButton.querySelector(".tool-label").textContent =
    state.largeText ? ui("largerTextOn") : ui("largerText");
  refs.motionButton.querySelector(".tool-label").textContent =
    state.reduceMotion ? ui("reduceMotionOn") : ui("reduceMotion");
  refs.exportButton.querySelector("span:last-child").textContent = ui("export");
}

function showFatal(error) {
  refs.loading.hidden = true;
  refs.shell.hidden = true;
  refs.errorScreen.hidden = false;
  refs.errorMessage.textContent =
    error instanceof Error && error.message ? error.message : ui("loadFailure");
}

function setLoading() {
  refs.errorScreen.hidden = true;
  refs.shell.hidden = true;
  refs.loading.hidden = false;
  refs.loading.querySelector("p").textContent = ui("loading");
}

function renderPackSelect() {
  if (!state.bootstrap) return;
  refs.packSelect.replaceChildren();
  for (const pack of state.bootstrap.packs) {
    const option = node("option", "", localized(pack.title));
    option.value = pack.id;
    refs.packSelect.append(option);
  }
  refs.packSelect.value = state.pack?.id || state.bootstrap.default_pack_id;
}

function renderNav() {
  refs.lessonList.replaceChildren();
  if (!state.pack) return;
  const progress = state.pack.progress || {};
  for (const [index, lesson] of state.pack.lessons.entries()) {
    const button = node("button", "lesson-nav-item");
    button.type = "button";
    button.setAttribute("aria-current", index === state.lessonIndex ? "true" : "false");
    button.dataset.testid = "lesson-nav-item";
    const number = node("span", "lesson-nav-number", String(index + 1).padStart(2, "0"));
    const box = node("span", "lesson-nav-copy");
    box.append(node("strong", "", localized(lesson.title)));
    const small = node("small");
    small.append(document.createTextNode(localized(lesson.duration)));
    const stats = progress[lesson.id];
    if (stats) {
      const score = node(
        "span",
        "lesson-practiced",
        `${stats.best_score}/${stats.total}`
      );
      score.title = `${ui("best")} ${stats.best_score}/${stats.total}`;
      small.append(score);
    }
    box.append(small);
    button.append(number, box);
    button.addEventListener("click", () => {
      selectLesson(index);
    });
    refs.lessonList.append(button);
  }
  const practiced = Object.keys(progress).length;
  refs.courseProgress.textContent = `${practiced} / ${state.pack.lessons.length} ${ui("studied")}`;
}

function renderLessonHeader(lesson) {
  const header = node("header", "lesson-header");
  const kickerRow = node("div", "lesson-kicker-row");
  kickerRow.append(
    node("span", "lesson-kicker", localized(lesson.kicker)),
    node(
      "span",
      "lesson-tag",
      state.pack.origin === "imported" ? ui("importedTag") : ui("authored")
    )
  );
  const title = node("h1", "", localized(lesson.title));
  title.id = "active-lesson-title";
  const summary = node("p", "lesson-summary", localized(lesson.summary));
  const meta = node("div", "lesson-meta");
  meta.append(
    node("span", "", localized(lesson.duration)),
    node(
      "span",
      "",
      `${lesson.questions?.length || 0} ${ui("checks")}`
    ),
    node(
      "span",
      "",
      `${sourceCodes(lesson).size} ${
        sourceCodes(lesson).size === 1 ? ui("sourceOne") : ui("sourceMany")
      }`
    )
  );
  append(header, kickerRow, title, summary, meta);
  return header;
}

function sourceCodes(lesson) {
  const codes = new Set();
  for (const block of lesson.body || []) {
    if (block.source) codes.add(block.source);
  }
  for (const question of lesson.questions || []) {
    if (question.source) codes.add(question.source);
  }
  return codes;
}

function sourceButton(code, quiet = false) {
  const button = node(
    "button",
    quiet ? "result-source" : "source-anchor",
    quiet ? `${ui("sourceBack")} ${code}` : `${ui("source")} ${code}`
  );
  button.type = "button";
  button.dataset.sourceJump = code;
  button.addEventListener("click", () => openSource(code));
  return button;
}

function renderReading(lesson) {
  const section = node("section", "content-section reading-section");
  section.setAttribute("aria-labelledby", "active-lesson-title");
  for (const block of lesson.body || []) {
    const wrapper = node(
      "div",
      `reading-block${block.kind === "lead" ? " lead-read" : ""}${
        block.kind === "callout" ? " callout-read" : ""
      }`
    );
    if (block.kind === "callout") {
      wrapper.append(node("h3", "", localized(block.title)));
      wrapper.append(node("p", "", localized(block.text)));
    } else {
      wrapper.append(node("p", "", localized(block.text)));
    }
    if (block.source) wrapper.append(sourceButton(block.source));
    section.append(wrapper);
  }
  section.append(node("p", "empty-practice", ui("readingNote")));
  return section;
}

function openSource(code) {
  const source = refs.lessonView.querySelector(`[data-source-card="${code}"]`);
  if (!source) return;
  source.open = true;
  source.scrollIntoView({ block: "center", behavior: state.reduceMotion ? "auto" : "smooth" });
  source.querySelector("summary")?.focus({ preventScroll: true });
}

function renderSources(lesson) {
  const section = node("section", "content-section");
  section.setAttribute("aria-labelledby", "sources-title");
  const heading = node("div", "section-heading");
  const titleBox = node("div");
  titleBox.append(
    node("p", "micro-label", `${ui("source")} map`),
    node("h2", "", ui("sourceTitle"))
  );
  titleBox.querySelector("h2").id = "sources-title";
  heading.append(titleBox, node("p", "", ui("sourceSubtitle")));
  const stack = node("div", "source-stack");
  const codes = sourceCodes(lesson);
  for (const source of state.pack.sources.filter((item) => codes.has(item.code))) {
    const details = node("details", "source-item");
    details.dataset.sourceCard = source.code;
    const summary = node("summary");
    const summaryCopy = node("span", "source-summary-copy");
    summaryCopy.append(
      node("strong", "", localized(source.title)),
      node("small", "", localized(source.label))
    );
    summary.append(
      node("span", "source-code", source.code),
      summaryCopy
    );
    details.append(summary, node("blockquote", "source-passage", localized(source.text)));
    stack.append(details);
  }
  append(section, heading, stack);
  return section;
}

function traceVisual(lesson) {
  const visual = lesson.visual;
  const trace = visual.trace;
  const section = node("section", "content-section visual-panel");
  section.setAttribute("aria-labelledby", "visual-title");
  const heading = node("div", "section-heading");
  const titleBox = node("div");
  const title = node("h2", "", ui("interactiveTitle"));
  title.id = "visual-title";
  titleBox.append(
    node("p", "micro-label", "Dijkstra · live trace"),
    title
  );
  heading.append(titleBox, node("p", "", ui("interactiveSubtitle")));

  const currentStepIndex = Math.min(state.step, trace.steps.length - 1);
  const currentStep = trace.steps[currentStepIndex];
  const isFinal = currentStepIndex === trace.steps.length - 1;
  const finalEdges = new Set();
  if (isFinal && trace.path.length > 1) {
    for (let index = 0; index < trace.path.length - 1; index += 1) {
      finalEdges.add([trace.path[index], trace.path[index + 1]].sort().join("|"));
    }
  }

  const frame = node("div", "graph-frame");
  const svg = svgNode("svg", {
    class: "graph-svg",
    viewBox: "0 0 648 432",
    role: "img",
    "aria-labelledby": "graph-title graph-desc"
  });
  const graphTitle = svgNode("title", { id: "graph-title" });
  graphTitle.textContent = ui("interactiveTitle");
  const graphDesc = svgNode("desc", { id: "graph-desc" });
  graphDesc.textContent = `Dijkstra ${ui("step")} ${currentStepIndex + 1}. ${
    currentStep.current ? `${ui("current")}: ${currentStep.current}.` : ""
  }`;
  svg.append(graphTitle, graphDesc);

  const byId = new Map(visual.nodes.map((item) => [item.id, item]));
  for (const edge of visual.edges) {
    const from = byId.get(edge.from);
    const to = byId.get(edge.to);
    if (!from || !to) continue;
    const key = [edge.from, edge.to].sort().join("|");
    const line = svgNode("line", {
      x1: from.x,
      y1: from.y,
      x2: to.x,
      y2: to.y,
      class: `edge${finalEdges.has(key) ? " edge--path" : ""}`
    });
    svg.append(line);
    const midX = (from.x + to.x) / 2;
    const midY = (from.y + to.y) / 2;
    svg.append(
      svgNode("rect", {
        x: midX - 13,
        y: midY - 11,
        width: 26,
        height: 22,
        rx: 5,
        class: "edge-weight-bg"
      })
    );
    const weight = svgNode("text", {
      x: midX,
      y: midY + 4,
      class: "edge-weight"
    });
    weight.textContent = String(edge.weight);
    svg.append(weight);
  }

  for (const item of visual.nodes) {
    const isCurrent = currentStep.current === item.id;
    const isSettled = currentStep.settled.includes(item.id);
    const group = svgNode("g", {
      class: `graph-node${isSettled ? " is-settled" : ""}${
        isCurrent ? " is-current" : ""
      }${item.id === visual.goal ? " is-goal" : ""}`,
      transform: `translate(${item.x} ${item.y})`
    });
    group.append(svgNode("circle", { r: 24 }));
    const idText = svgNode("text", { y: 4, class: "node-id" });
    idText.textContent = item.id;
    const labelText = svgNode("text", { y: 42, class: "node-label" });
    labelText.textContent = localized(item.label);
    append(group, idText, labelText);
    svg.append(group);
  }

  const toolbar = node("div", "step-toolbar");
  const reset = node("button", "step-button", ui("reset"));
  reset.type = "button";
  reset.dataset.graphAction = "reset";
  reset.disabled = currentStepIndex === 0;
  const back = node("button", "step-button", ui("back"));
  back.type = "button";
  back.dataset.graphAction = "back";
  back.disabled = currentStepIndex === 0;
  const next = node("button", "step-button step-button--primary", ui("next"));
  next.type = "button";
  next.dataset.graphAction = "next";
  next.disabled = isFinal;
  for (const [button, action] of [
    [reset, "reset"],
    [back, "back"],
    [next, "next"]
  ]) {
    button.addEventListener("click", () => setGraphStep(action));
  }
  const status = node(
    "span",
    "step-status",
    `${ui("step")} ${currentStepIndex + 1} / ${trace.steps.length}`
  );
  status.dataset.testid = "step-status";
  status.setAttribute("aria-live", "polite");
  append(toolbar, reset, back, next, status);
  append(frame, svg, toolbar);

  const readout = node("div", "graph-readout");
  const distancesPane = node("div", "readout-pane");
  distancesPane.append(node("p", "readout-title", ui("distances")));
  const distanceList = node("div", "distance-list");
  for (const item of visual.nodes) {
    const distance = currentStep.distances[item.id];
    const pill = node(
      "span",
      `distance-pill${currentStep.settled.includes(item.id) ? " is-settled" : ""}${
        currentStep.current === item.id ? " is-current" : ""
      }`,
      `${item.id} ${distance === null ? "∞" : distance}`
    );
    distanceList.append(pill);
  }
  distancesPane.append(distanceList);

  const relaxPane = node("div", "readout-pane");
  relaxPane.append(node("p", "readout-title", ui("relaxations")));
  const log = node("div", "relaxation-log");
  if (currentStep.relaxations.length) {
    for (const relaxation of currentStep.relaxations) {
      log.append(
        node(
          "p",
          "",
          `${relaxation.from} → ${relaxation.to}: ${
            relaxation.previous === null ? "∞" : relaxation.previous
          } → ${relaxation.distance}`
        )
      );
    }
  } else {
    log.append(node("p", "", ui("noRelax")));
  }
  if (isFinal) {
    const verdict = node(
      "p",
      "graph-verdict",
      trace.path.length
        ? `${ui("path")}: ${trace.path.join(" → ")} · ${ui("cost")} ${trace.distance}`
        : ui("unreachable")
    );
    verdict.dataset.testid = "path-verdict";
    log.append(verdict);
  }
  relaxPane.append(log);
  append(readout, distancesPane, relaxPane);
  append(section, heading, frame, readout);
  state.visualSection = section;
  return section;
}

function setGraphStep(action) {
  const lesson = currentLesson();
  const trace = lesson?.visual?.trace;
  if (!trace) return;
  if (action === "reset") state.step = 0;
  if (action === "back") state.step = Math.max(0, state.step - 1);
  if (action === "next") state.step = Math.min(trace.steps.length - 1, state.step + 1);
  if (!state.visualSection) return;
  const existing = state.visualSection;
  const replacement = traceVisual(lesson);
  existing.replaceWith(replacement);
  const control = replacement.querySelector(`[data-graph-action="${action}"]`);
  if (control && !control.disabled) {
    control.focus({ preventScroll: true });
  } else {
    replacement.querySelector("[data-graph-action='back']")?.focus({ preventScroll: true });
  }
}

function renderPractice(lesson) {
  const section = node("section", "content-section");
  section.setAttribute("aria-labelledby", "practice-title");
  const heading = node("div", "section-heading");
  const titleBox = node("div");
  const title = node("h2", "", ui("practiceTitle"));
  title.id = "practice-title";
  titleBox.append(
    node("p", "micro-label", "Retrieval · source-backed"),
    title
  );
  heading.append(titleBox, node("p", "", ui("practiceSubtitle")));
  section.append(heading);

  const questions = lesson.questions || [];
  if (!questions.length) {
    section.append(node("p", "empty-practice", ui("noPractice")));
    return section;
  }

  const intro = node("div", "quiz-intro-line");
  intro.append(
    node(
      "p",
      "",
      `${questions.length} ${
        questions.length === 1 ? ui("practiceIntroOne") : ui("practiceIntroMany")
      } · ${ui("practiceIntroEnd")}`
    ),
    node("span", "quiz-type", ui("practiceType"))
  );
  section.append(intro);

  const form = node("form", "quiz-form");
  form.id = "quiz-form";
  form.dataset.testid = "practice-form";
  form.noValidate = true;
  for (const [index, question] of questions.entries()) {
    const card = node("div", "question-card");
    card.dataset.questionId = question.id;
    const fieldset = node("fieldset");
    const legend = node("legend");
    legend.append(
      node("span", "question-index", String(index + 1).padStart(2, "0")),
      document.createTextNode(localized(question.prompt))
    );
    fieldset.append(legend);
    for (const option of question.options) {
      const label = node("label", "option-row");
      const input = node("input");
      input.type = "radio";
      input.name = question.id;
      input.value = option.id;
      input.dataset.optionId = option.id;
      label.append(input, node("span", "", localized(option.text)));
      fieldset.append(label);
    }
    card.append(fieldset);
    form.append(card);
  }

  const actions = node("div", "quiz-actions");
  const submit = node("button", "primary-button", ui("submit"));
  submit.type = "submit";
  submit.id = "quiz-submit";
  submit.dataset.testid = "submit-answers";
  const status = node("span", "form-status");
  status.setAttribute("role", "alert");
  status.dataset.testid = "quiz-status";
  actions.append(submit, status);
  form.append(actions);

  const results = node("div", "quiz-results");
  results.dataset.testid = "practice-results";
  results.hidden = true;
  results.setAttribute("aria-live", "polite");
  section.append(form, results);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (state.submitBusy) return;
    status.textContent = "";
    const data = new FormData(form);
    const answers = {};
    let missing = null;
    for (const question of questions) {
      const selected = data.get(question.id);
      if (!selected) {
        missing = question.id;
        break;
      }
      answers[question.id] = String(selected);
    }
    if (missing) {
      status.textContent = ui("incomplete");
      form.querySelector(`input[name="${missing}"]`)?.focus();
      return;
    }

    state.submitBusy = true;
    submit.disabled = true;
    submit.textContent = ui("checking");
    form.setAttribute("aria-busy", "true");
    try {
      const response = await api("/api/attempts", {
        method: "POST",
        body: {
          pack_id: state.pack.id,
          lesson_id: lesson.id,
          answers
        }
      });
      const previous = state.pack.progress[lesson.id];
      state.pack.progress[lesson.id] = {
        attempts: (previous?.attempts || 0) + 1,
        best_score: Math.max(previous?.best_score || 0, response.score),
        total: response.total
      };
      renderNav();
      renderAttemptResults(lesson, response, results);
      results.hidden = false;
      state.reviewItems = [];
      refs.reviewCount.textContent = String(response.review_count);
      refs.reviewCount.classList.toggle("has-items", response.review_count > 0);
      await refreshReviews();
      results.scrollIntoView({
        block: "nearest",
        behavior: state.reduceMotion ? "auto" : "smooth"
      });
    } catch (error) {
      status.textContent = error instanceof Error ? error.message : ui("loadFailure");
    } finally {
      state.submitBusy = false;
      submit.disabled = false;
      submit.textContent = ui("submit");
      form.removeAttribute("aria-busy");
    }
  });

  return section;
}

function renderAttemptResults(lesson, response, container) {
  container.replaceChildren();
  const wrong = response.results.filter((result) => !result.is_correct).length;
  const banner = node("div", `score-banner${wrong ? " is-low" : ""}`);
  const scoreCopy = node("div", "score-copy");
  scoreCopy.append(
    node(
      "strong",
      "",
      `${ui("score")} ${response.score} / ${response.total} ${ui("scoreEnd")}`
    ),
    node(
      "small",
      "",
      wrong
        ? `${wrong} ${
            wrong === 1 ? ui("wrongAddedOne") : ui("wrongAddedMany")
          }`
        : ui("noWrong")
    )
  );
  const retry = node("button", "text-button", ui("tryAgain"));
  retry.type = "button";
  retry.dataset.testid = "retry-practice";
  retry.addEventListener("click", () => {
    container.hidden = true;
    container.replaceChildren();
    refs.lessonView.querySelectorAll("#quiz-form input[type='radio']").forEach((input) => {
      input.checked = false;
    });
    refs.lessonView.querySelector("#quiz-form input[type='radio']")?.focus();
  });
  banner.append(
    node("span", "score-number", `${response.score}/${response.total}`),
    scoreCopy,
    retry
  );

  const resultList = node("div", "result-list");
  for (const result of response.results) {
    const question = lesson.questions.find((item) => item.id === result.question_id);
    const selected = question?.options.find((item) => item.id === result.selected_option);
    const correct = question?.options.find((item) => item.id === result.correct_option);
    const card = node("div", `result-card${result.is_correct ? "" : " is-incorrect"}`);
    card.dataset.testid = result.is_correct ? "result-correct" : "result-incorrect";
    const head = node("div", "result-head");
    head.append(
      node("span", "result-mark", result.is_correct ? "✓" : "!"),
      node("span", "", result.is_correct ? ui("correct") : ui("incorrect"))
    );
    card.append(head);
    if (!result.is_correct && selected) {
      card.append(node("p", "", `${ui("yourAnswer")}: ${localized(selected.text)}`));
    }
    if (correct) {
      card.append(node("p", "", `${ui("correctAnswer")}: ${localized(correct.text)}`));
    }
    const explanation = node("p");
    explanation.append(
      node("strong", "", `${ui("explanation")}: `),
      document.createTextNode(localized(result.explanation))
    );
    card.append(explanation);
    card.append(sourceButton(result.source.code, true));
    resultList.append(card);
  }
  container.append(banner, resultList);
}

function renderPager() {
  const pager = node("nav", "lesson-pager");
  pager.setAttribute("aria-label", "Lesson pages");
  const previousIndex = state.lessonIndex - 1;
  const nextIndex = state.lessonIndex + 1;
  if (previousIndex >= 0) {
    const previous = node("button", "pager-button");
    previous.type = "button";
    previous.append(
      node("small", "", `← ${ui("previous")}`),
      node("strong", "", localized(state.pack.lessons[previousIndex].title))
    );
    previous.addEventListener("click", () => selectLesson(previousIndex));
    pager.append(previous);
  } else {
    pager.append(node("span", "pager-spacer"));
  }
  if (nextIndex < state.pack.lessons.length) {
    const next = node("button", "pager-button");
    next.type = "button";
    next.append(
      node("small", "", `${ui("nextLesson")} →`),
      node("strong", "", localized(state.pack.lessons[nextIndex].title))
    );
    next.addEventListener("click", () => selectLesson(nextIndex));
    pager.append(next);
  } else {
    pager.append(node("span", "pager-spacer"));
  }
  return pager;
}

function renderLesson(focus = false) {
  const lesson = currentLesson();
  if (!lesson) {
    refs.lessonView.replaceChildren(
      node("p", "inline-error", ui("packFailure"))
    );
    return;
  }
  const article = node("article", "lesson-page");
  article.tabIndex = -1;
  article.append(renderLessonHeader(lesson), renderReading(lesson));
  if (lesson.visual?.type === "dijkstra") {
    article.append(traceVisual(lesson));
  }
  article.append(renderSources(lesson), renderPractice(lesson), renderPager());
  refs.lessonView.replaceChildren(article);
  document.title = `${localized(lesson.title)} · ${localized(state.pack.title)}`;
  if (focus) article.focus({ preventScroll: true });
}

function selectLesson(index, options = {}) {
  if (!state.pack || index < 0 || index >= state.pack.lessons.length) return;
  state.lessonIndex = index;
  state.step = 0;
  writeStorage(STORAGE.lesson, `${state.pack.id}:${state.pack.lessons[index].id}`);
  renderNav();
  renderLesson(options.focus !== false);
  if (options.scroll !== false) {
    const target = refs.mainContent.getBoundingClientRect().top + window.scrollY - 82;
    window.scrollTo({
      top: Math.max(0, target),
      behavior: state.reduceMotion ? "auto" : "smooth"
    });
  }
}

function renderReview() {
  const count = state.reviewItems.length;
  refs.reviewCount.textContent = String(count);
  refs.reviewCount.classList.toggle("has-items", count > 0);
  refs.reviewCount.setAttribute("aria-label", `${ui("openReviewAria")}: ${count}`);
  refs.reviewEmpty.hidden = count > 0;
  refs.reviewList.replaceChildren();
  for (const item of state.reviewItems) {
    const card = node("article", "review-item");
    card.dataset.testid = "review-item";
    card.dataset.reviewId = item.id;
    const top = node("div", "review-item-top");
    top.append(
      node("span", "review-source-code", item.source.code),
      node(
        "span",
        "review-attempts",
        `${item.attempts} ${item.attempts === 1 ? ui("reviewAttempt") : ui("reviewAttempts")}`
      )
    );
    card.append(
      top,
      node("strong", "", localized(item.prompt)),
      node("p", "review-concept", localized(item.concept))
    );
    const actions = node("div", "review-actions");
    const open = node("button", "review-action", ui("reviewOpen"));
    open.type = "button";
    open.dataset.testid = "review-open";
    open.addEventListener("click", async () => {
      try {
        await openPack(item.pack_id, item.lesson_id);
      } catch (error) {
        showToast(error.message || ui("packFailure"), true);
      }
    });
    const resolve = node("button", "review-action review-action--quiet", ui("reviewDone"));
    resolve.type = "button";
    resolve.dataset.testid = "review-resolve";
    resolve.addEventListener("click", async () => {
      resolve.disabled = true;
      try {
        await api(`/api/review/${item.id}/resolve`, {
          method: "POST",
          body: {}
        });
        await refreshReviews();
        showToast(ui("reviewResolved"));
      } catch (error) {
        resolve.disabled = false;
        showToast(error.message || ui("loadFailure"), true);
      }
    });
    actions.append(open, resolve);
    card.append(actions);
    refs.reviewList.append(card);
  }
}

async function refreshReviews() {
  const review = await api("/api/review");
  state.reviewItems = review.items || [];
  renderReview();
}

function allPacks() {
  return state.bootstrap?.packs || [];
}

async function refreshBootstrap() {
  state.bootstrap = await api("/api/bootstrap");
  renderPackSelect();
}

async function openPack(packId, lessonId = null, options = {}) {
  refs.packSelect.disabled = true;
  try {
    const [packResponse, review] = await Promise.all([
      api(`/api/packs/${encodeURIComponent(packId)}`),
      api("/api/review")
    ]);
    state.pack = packResponse.pack;
    state.reviewItems = review.items || [];
    const stored = readStorage(STORAGE.lesson);
    let preferredId = lessonId;
    if (!preferredId && stored?.startsWith(`${packId}:`)) {
      preferredId = stored.slice(packId.length + 1);
    }
    const foundIndex = state.pack.lessons.findIndex((lesson) => lesson.id === preferredId);
    state.lessonIndex = foundIndex >= 0 ? foundIndex : 0;
    state.step = 0;
    writeStorage(STORAGE.pack, packId);
    writeStorage(
      STORAGE.lesson,
      `${packId}:${state.pack.lessons[state.lessonIndex].id}`
    );
    refs.packSelect.value = packId;
    refs.loading.hidden = true;
    refs.errorScreen.hidden = true;
    refs.shell.hidden = false;
    renderStaticCopy();
    renderPackSelect();
    renderNav();
    renderLesson(Boolean(options.focus));
    renderReview();
  } finally {
    refs.packSelect.disabled = false;
  }
}

function showToast(message, isError = false) {
  window.clearTimeout(state.toastTimer);
  refs.toast.textContent = message;
  refs.toast.classList.toggle("is-error", isError);
  refs.toast.classList.add("is-visible");
  state.toastTimer = window.setTimeout(() => {
    refs.toast.classList.remove("is-visible");
  }, 3600);
}

function setImportBusy(busy) {
  refs.importSubmit.disabled = busy;
  refs.importForm.setAttribute("aria-busy", String(busy));
  refs.importSubmit.textContent = busy ? ui("importBuilding") : ui("importBuild");
}

function openImportDialog() {
  refs.importStatus.textContent = "";
  setImportBusy(false);
  if (!refs.dialog.open) refs.dialog.showModal();
  window.setTimeout(() => refs.importTitle.focus(), 30);
}

function closeImportDialog() {
  if (refs.dialog.open) refs.dialog.close();
}

async function submitImport(event) {
  event.preventDefault();
  if (refs.importSubmit.disabled) return;
  refs.importStatus.textContent = "";
  const text = refs.importText.value.trim();
  if (!text) {
    refs.importStatus.textContent = ui("importEmpty");
    refs.importText.focus();
    return;
  }
  setImportBusy(true);
  try {
    const response = await api("/api/import", {
      method: "POST",
      body: {
        title: refs.importTitle.value.trim(),
        text
      }
    });
    await refreshBootstrap();
    closeImportDialog();
    await openPack(response.pack_id, null, { focus: true });
    refs.importForm.reset();
    refs.importSize.textContent = "0 / 150,000";
    showToast(ui("importSuccess"));
    selectLesson(0);
  } catch (error) {
    refs.importStatus.textContent =
      error instanceof Error ? error.message : ui("loadFailure");
  } finally {
    setImportBusy(false);
  }
}

async function exportCurrentPack() {
  if (!state.pack || refs.exportButton.disabled) return;
  refs.exportButton.disabled = true;
  refs.exportButton.setAttribute("aria-busy", "true");
  const label = refs.exportButton.querySelector("span:last-child");
  label.textContent = ui("exporting");
  try {
    const response = await fetch(
      `/api/export/${encodeURIComponent(state.pack.id)}?lang=${state.lang}`
    );
    if (!response.ok) {
      let message = ui("exportFailure");
      try {
        const payload = await response.json();
        message = payload?.error?.message || message;
      } catch {
        // Keep the localized fallback when the error body is not JSON.
      }
      throw new Error(message);
    }
    const blob = await response.blob();
    const disposition = response.headers.get("Content-Disposition") || "";
    const filenameMatch = disposition.match(/filename=\"?([^\";]+)\"?/i);
    const filename =
      filenameMatch?.[1] || `SourceLoop-${state.pack.id}-${state.lang}.html`;
    const url = URL.createObjectURL(blob);
    const anchor = node("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.hidden = true;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 2000);
    showToast(ui("exportSuccess"));
  } catch (error) {
    showToast(error instanceof Error ? error.message : ui("exportFailure"), true);
  } finally {
    refs.exportButton.disabled = false;
    refs.exportButton.removeAttribute("aria-busy");
    label.textContent = ui("export");
  }
}

async function initialize() {
  applyPreferences();
  setLoading();
  try {
    await refreshBootstrap();
    const validPack = allPacks().some((pack) => pack.id === readStorage(STORAGE.pack));
    const packId = validPack
      ? readStorage(STORAGE.pack)
      : state.bootstrap.default_pack_id;
    await openPack(packId);
  } catch (error) {
    showFatal(error);
  }
}

refs.langButton.addEventListener("click", () => {
  state.lang = state.lang === "en" ? "zh" : "en";
  writeStorage(STORAGE.language, state.lang);
  renderStaticCopy();
  if (state.pack) {
    renderPackSelect();
    renderNav();
    renderLesson(false);
    renderReview();
  }
});

refs.textButton.addEventListener("click", () => {
  state.largeText = !state.largeText;
  writeStorage(STORAGE.largeText, String(state.largeText));
  renderStaticCopy();
});

refs.motionButton.addEventListener("click", () => {
  state.reduceMotion = !state.reduceMotion;
  writeStorage(STORAGE.reduceMotion, String(state.reduceMotion));
  renderStaticCopy();
});

refs.packSelect.addEventListener("change", async () => {
  try {
    await openPack(refs.packSelect.value, null, { focus: true });
  } catch (error) {
    refs.packSelect.value = state.pack?.id || "";
    showToast(error.message || ui("packFailure"), true);
  }
});

refs.exportButton.addEventListener("click", exportCurrentPack);
refs.retryLoad.addEventListener("click", initialize);
refs.importOpen.addEventListener("click", openImportDialog);
refs.importCard.addEventListener("click", openImportDialog);
refs.reviewImport.addEventListener("click", openImportDialog);
refs.importCancel.addEventListener("click", closeImportDialog);
refs.importClose.addEventListener("click", closeImportDialog);
refs.importForm.addEventListener("submit", submitImport);
refs.importText.addEventListener("input", () => {
  refs.importSize.textContent = `${refs.importText.value.length.toLocaleString()} / 150,000`;
});
refs.importFile.addEventListener("change", async () => {
  const file = refs.importFile.files?.[0];
  if (!file) return;
  refs.importStatus.textContent = "";
  try {
    const text = await file.text();
    refs.importText.value = text;
    if (!refs.importTitle.value.trim()) {
      refs.importTitle.value = file.name.replace(/\.(md|markdown|txt)$/i, "");
    }
    refs.importSize.textContent = `${text.length.toLocaleString()} / 150,000`;
  } catch {
    refs.importStatus.textContent = ui("importUnreadable");
  }
});
refs.dialog.addEventListener("click", (event) => {
  if (event.target !== refs.dialog) return;
  const rect = refs.dialog.getBoundingClientRect();
  const inside =
    event.clientX >= rect.left &&
    event.clientX <= rect.right &&
    event.clientY >= rect.top &&
    event.clientY <= rect.bottom;
  if (!inside) closeImportDialog();
});

renderStaticCopy();
initialize();
