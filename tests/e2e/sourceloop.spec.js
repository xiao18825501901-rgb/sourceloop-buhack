const { test, expect } = require("@playwright/test");
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const EVIDENCE = path.resolve("evidence");
const FIXTURE = path.resolve("fixtures/import-demo.md");

test.beforeAll(async ({ request }) => {
  fs.mkdirSync(EVIDENCE, { recursive: true });
  const response = await request.get("/api/review");
  expect(response.ok()).toBeTruthy();
  const review = await response.json();
  for (const item of review.items) {
    const resolved = await request.post(`/api/review/${item.id}/resolve`, {
      data: {}
    });
    expect(resolved.ok()).toBeTruthy();
  }
});

test("desktop learning loop, live trace, grading, export, and offline use", async ({
  page,
  browser
}) => {
  const browserErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") browserErrors.push(message.text());
  });
  page.on("pageerror", (error) => browserErrors.push(error.message));

  await page.goto("/");
  await expect(page.locator("#app-shell")).toBeVisible();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Read before you run"
  );
  await expect(page.locator("#review-count")).toHaveText("0");
  await page.keyboard.press("Tab");
  await expect(page.locator(".skip-link")).toBeFocused();

  await page.locator("#lang-button").click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("先读懂，再计算");
  await expect(page.locator("html")).toHaveAttribute("lang", "zh");
  await page.locator("#lang-button").click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Read before you run"
  );

  await page.locator("#text-button").click();
  await expect(page.locator("html")).toHaveAttribute("data-text-size", "large");
  await expect(page.locator("#text-button")).toHaveAttribute("aria-pressed", "true");
  await page.locator("#text-button").click();

  await page.locator("#motion-button").click();
  await expect(page.locator("html")).toHaveAttribute("data-reduced-motion", "true");
  await expect(page.locator("#motion-button")).toHaveAttribute("aria-pressed", "true");

  await page.locator("button.source-anchor").first().click();
  await expect(
    page.locator('details.source-item[data-source-card="S1"]')
  ).toHaveAttribute("open", "");
  await expect(
    page.locator('details.source-item[data-source-card="S1"] blockquote')
  ).toContainText("A weighted graph is a set of places");

  await page
    .locator('[data-testid="lesson-nav-item"]')
    .filter({ hasText: "The frontier tells the truth" })
    .click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "The frontier tells the truth"
  );
  await expect(page.locator('[data-testid="step-status"]')).toHaveText("Step 1 / 6");

  const next = page.locator('[data-graph-action="next"]');
  await next.click();
  await expect(next).toBeFocused();
  await expect(page.locator('[data-testid="step-status"]')).toHaveText("Step 2 / 6");
  for (let index = 0; index < 8 && (await next.isEnabled()); index += 1) {
    await next.click();
  }
  await expect(page.locator('[data-testid="step-status"]')).toHaveText("Step 6 / 6");
  await expect(page.locator('[data-testid="path-verdict"]')).toHaveText(
    "Shortest path: LIB → CAN → LAB · cost 9"
  );
  await page.locator(".visual-panel").scrollIntoViewIfNeeded();
  await page.screenshot({
    path: path.join(EVIDENCE, "ui-graph-desktop.png"),
    fullPage: false
  });

  await page.locator('input[name="next-node"][value="b"]').check();
  await page.locator('input[name="settled-safety"][value="b"]').check();
  await page.locator('input[name="relaxation"][value="c"]').check();
  await page.locator('[data-testid="submit-answers"]').click();
  await expect(page.locator('[data-testid="result-incorrect"]')).toHaveCount(1);
  await expect(page.locator("#review-count")).toHaveText("1");
  await expect(page.locator('[data-testid="review-item"]')).toHaveCount(1);
  await expect(page.locator('[data-testid="review-item"]')).toContainText("S3");

  await page.locator('[data-testid="retry-practice"]').click();
  await page.locator('input[name="next-node"][value="a"]').check();
  await page.locator('input[name="settled-safety"][value="b"]').check();
  await page.locator('input[name="relaxation"][value="c"]').check();
  await page.locator('[data-testid="submit-answers"]').click();
  await expect(page.locator('[data-testid="result-correct"]')).toHaveCount(3);
  await expect(page.locator("#review-count")).toHaveText("0");
  await expect(page.locator("#review-empty")).toBeVisible();
  await page.locator(".score-banner").scrollIntoViewIfNeeded();
  await page.screenshot({
    path: path.join(EVIDENCE, "ui-practice-feedback.png"),
    fullPage: false
  });

  await page
    .locator('[data-testid="lesson-nav-item"]')
    .filter({ hasText: "Know when the shortcut fails" })
    .click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Know when the shortcut fails"
  );
  await expect(page.locator("body")).toContainText("No edge may have a negative weight");

  await page
    .locator('[data-testid="lesson-nav-item"]')
    .filter({ hasText: "The frontier tells the truth" })
    .click();
  await page.locator(".lesson-header").scrollIntoViewIfNeeded();
  await page.screenshot({
    path: path.join(EVIDENCE, "ui-desktop-1440.png"),
    fullPage: false
  });

  const downloadPromise = page.waitForEvent("download");
  await page.locator("#export-button").click();
  const download = await downloadPromise;
  const exportPath = path.join(EVIDENCE, "SourceLoop-campus-routes-en.html");
  await download.saveAs(exportPath);
  expect(fs.statSync(exportPath).size).toBeGreaterThan(50_000);

  const offlineContext = await browser.newContext({
    offline: true,
    viewport: { width: 1280, height: 900 },
    locale: "en-US"
  });
  const offlinePage = await offlineContext.newPage();
  const offlineErrors = [];
  offlinePage.on("console", (message) => {
    if (message.type() === "error") offlineErrors.push(message.text());
  });
  offlinePage.on("pageerror", (error) => offlineErrors.push(error.message));
  await offlinePage.goto(pathToFileURL(exportPath).href);
  await expect(offlinePage.getByRole("heading", { level: 1 })).toHaveText(
    "Campus Routes Lab"
  );
  await offlinePage
    .locator(".lesson-button")
    .filter({ hasText: "The frontier tells the truth" })
    .click();
  const offlineNext = offlinePage.locator("#next-step");
  for (let index = 0; index < 8 && (await offlineNext.isEnabled()); index += 1) {
    await offlineNext.click();
  }
  await expect(offlinePage.locator("#relaxation-log")).toContainText(
    "Shortest path: Library → Canteen → Lab · 9"
  );
  await offlinePage.locator('input[name="next-node"][value="b"]').check();
  await offlinePage.locator('input[name="settled-safety"][value="b"]').check();
  await offlinePage.locator('input[name="relaxation"][value="c"]').check();
  await offlinePage.locator(".submit-button").click();
  await expect(offlinePage.locator(".result.incorrect")).toHaveCount(1);
  await offlinePage.screenshot({
    path: path.join(EVIDENCE, "ui-offline-file.png"),
    fullPage: false
  });
  await offlineContext.close();

  expect(browserErrors).toEqual([]);
  expect(offlineErrors).toEqual([]);
});

test("390 and 320 pixel layouts have no horizontal overflow", async ({ page }) => {
  const errors = [];
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  page.on("pageerror", (error) => errors.push(error.message));

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(page.locator("#app-shell")).toBeVisible();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Read before you run"
  );
  let dimensions = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.innerWidth + 1);

  await page
    .locator('[data-testid="lesson-nav-item"]')
    .filter({ hasText: "The frontier tells the truth" })
    .click();
  await expect(page.locator(".graph-svg")).toBeVisible();
  await page.locator("#lang-button").click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("边界为什么可信");
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: path.join(EVIDENCE, "ui-mobile-390.png"),
    fullPage: false
  });

  await page.setViewportSize({ width: 320, height: 760 });
  dimensions = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.innerWidth + 1);
  await expect(page.locator("#lang-button")).toBeVisible();
  await expect(page.locator("#export-button")).toBeVisible();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: path.join(EVIDENCE, "ui-mobile-320.png"),
    fullPage: false
  });
  expect(errors).toEqual([]);
});

test("local Markdown import creates source checks that enter review", async ({
  page
}) => {
  const errors = [];
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  page.on("pageerror", (error) => errors.push(error.message));

  await page.goto("/");
  await expect(page.locator("#app-shell")).toBeVisible();
  await page.locator("#import-open").click();
  await expect(page.locator("#import-dialog")).toBeVisible();
  await page.locator("#import-file").setInputFiles(FIXTURE);
  await expect(page.locator("#import-title")).toHaveValue(
    "import-demo"
  );
  await expect(page.locator("#import-text")).toHaveValue(/Retrieval practice/);
  await page.locator("#import-submit").click();

  await expect(page.locator("#pack-select")).toHaveValue(/^import-/);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Encoding");
  await expect(page.locator(".source-item")).not.toHaveCount(0);
  await expect(page.getByText("Your local notes", { exact: true })).toBeVisible();

  await page.locator('input[name="quote-check"][value="b"]').check();
  const sourceLocation = page.locator('input[name="source-location"]');
  if (await sourceLocation.count()) {
    await sourceLocation.first().check();
  }
  await page.locator('[data-testid="submit-answers"]').click();
  await expect(page.locator('[data-testid="result-incorrect"]')).not.toHaveCount(0);
  await expect(page.locator('[data-testid="review-item"]')).not.toHaveCount(0);
  const reviewBefore = await page.locator('[data-testid="review-item"]').count();
  await page.screenshot({
    path: path.join(EVIDENCE, "ui-import-review.png"),
    fullPage: false
  });
  await page.locator('[data-testid="review-resolve"]').first().click();
  await expect(page.locator('[data-testid="review-item"]')).toHaveCount(
    Math.max(0, reviewBefore - 1)
  );
  expect(errors).toEqual([]);
});
