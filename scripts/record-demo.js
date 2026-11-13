const { chromium } = require("@playwright/test");
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const project = path.resolve(__dirname, "..");
const evidence = path.join(project, "evidence");
const temporaryVideoDir = path.join(evidence, "video-recording");
const fixture = path.join(project, "fixtures", "import-demo.md");
const baseUrl = process.env.SOURCELOOP_DEMO_URL || "http://127.0.0.1:8767";
const targetSeconds = Number(process.env.SOURCELOOP_DEMO_TARGET_SECONDS || "150");

function seconds(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function hold(page, milliseconds) {
  await page.waitForTimeout(milliseconds);
}

async function openLesson(page, title) {
  await page
    .locator('[data-testid="lesson-nav-item"]')
    .filter({ hasText: title })
    .click();
  await hold(page, 1200);
}

async function check(page, name, value) {
  await page.locator(`input[name="${name}"][value="${value}"]`).check();
}

(async () => {
  fs.mkdirSync(evidence, { recursive: true });
  fs.rmSync(temporaryVideoDir, { recursive: true, force: true });
  fs.mkdirSync(temporaryVideoDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    locale: "en-US",
    recordVideo: {
      dir: temporaryVideoDir,
      size: { width: 1280, height: 720 }
    }
  });
  const page = await context.newPage();
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") pageErrors.push(message.text());
  });

  const startedAt = Date.now();
  try {
    const reviewResponse = await page.request.get(`${baseUrl}/api/review`);
    if (reviewResponse.ok()) {
      const review = await reviewResponse.json();
      for (const item of review.items) {
        await page.request.post(`${baseUrl}/api/review/${item.id}/resolve`, {
          data: {}
        });
      }
    }

    await page.goto(`${baseUrl}/`);
    await page.locator("#app-shell").waitFor();
    await hold(page, 9000);

    await page.locator("button.source-anchor").first().click();
    await hold(page, 8000);

    await page.locator("#lang-button").click();
    await hold(page, 6000);
    await page.locator("#lang-button").click();
    await hold(page, 3000);

    await openLesson(page, "The frontier tells the truth");
    await page.locator('[data-testid="step-status"]').waitFor();
    await hold(page, 3500);
    const next = page.locator('[data-graph-action="next"]');
    for (let index = 0; index < 8 && (await next.isEnabled()); index += 1) {
      await next.click();
      await hold(page, 1500);
    }
    await hold(page, 6000);

    await check(page, "next-node", "b");
    await check(page, "settled-safety", "b");
    await check(page, "relaxation", "c");
    await hold(page, 2500);
    await page.locator('[data-testid="submit-answers"]').click();
    await page.locator('[data-testid="result-incorrect"]').first().waitFor();
    await hold(page, 6500);
    await page.locator('[data-testid="review-item"]').first().scrollIntoViewIfNeeded();
    await hold(page, 4500);

    await page.locator('[data-testid="retry-practice"]').click();
    await check(page, "next-node", "a");
    await check(page, "settled-safety", "b");
    await check(page, "relaxation", "c");
    await hold(page, 2000);
    await page.locator('[data-testid="submit-answers"]').click();
    await page.locator('[data-testid="result-correct"]').first().waitFor();
    await hold(page, 6500);

    await openLesson(page, "Know when the shortcut fails");
    await hold(page, 6500);
    await openLesson(page, "The frontier tells the truth");
    await hold(page, 2000);

    await page.locator("#import-open").click();
    await page.locator("#import-dialog").waitFor();
    await hold(page, 1200);
    await page.locator("#import-file").setInputFiles(fixture);
    await hold(page, 3500);
    await page.locator("#import-submit").click();
    await page.locator("#pack-select").waitFor();
    await hold(page, 6500);

    await page.locator("#pack-select").selectOption("campus-routes");
    await hold(page, 3000);

    const downloadPromise = page.waitForEvent("download");
    await page.locator("#export-button").click();
    const download = await downloadPromise;
    const exportPath = path.join(evidence, "SourceLoop-campus-routes-en.html");
    await download.saveAs(exportPath);
    await hold(page, 2500);

    await context.setOffline(true);
    await page.goto(pathToFileURL(exportPath).href);
    await page.locator("#lesson-title").waitFor();
    await hold(page, 4500);
    await page
      .locator(".lesson-button")
      .filter({ hasText: "The frontier tells the truth" })
      .click();
    await hold(page, 2000);
    const offlineNext = page.locator("#next-step");
    for (let index = 0; index < 8 && (await offlineNext.isEnabled()); index += 1) {
      await offlineNext.click();
      await hold(page, 700);
    }
    await page.locator('input[name="next-node"][value="b"]').check();
    await page.locator('input[name="settled-safety"][value="b"]').check();
    await page.locator('input[name="relaxation"][value="c"]').check();
    await page.locator(".submit-button").click();
    await page.locator(".result.incorrect").first().waitFor();
    await hold(page, 6500);
    await context.setOffline(false);

    await page.goto(`${baseUrl}/`);
    await page.locator("#app-shell").waitFor();
    await hold(page, 3000);

    const remaining = targetSeconds * 1000 - (Date.now() - startedAt);
    if (remaining > 0) {
      await hold(page, remaining);
    }
  } finally {
    const video = page.video();
    await context.close();
    if (video) {
      await video.saveAs(path.join(evidence, "SourceLoop-demo-raw.webm"));
    }
    await browser.close();
  }

  if (pageErrors.length) {
    throw new Error(`Browser errors during recording: ${pageErrors.join(" | ")}`);
  }

  console.log("Recorded evidence/SourceLoop-demo-raw.webm");
})();
