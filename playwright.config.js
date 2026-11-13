const { defineConfig } = require("@playwright/test");

const externalServer = process.env.SOURCELOOP_EXTERNAL_SERVER === "1";

module.exports = defineConfig({
  testDir: "./tests/e2e",
  timeout: 60_000,
  expect: {
    timeout: 10_000
  },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [
    ["list"],
    ["html", { outputFolder: "evidence/playwright-report", open: "never" }]
  ],
  use: {
    baseURL: "http://127.0.0.1:8766",
    headless: true,
    locale: "en-US",
    colorScheme: "light",
    acceptDownloads: true,
    trace: "retain-on-failure",
    screenshot: "only-on-failure"
  },
  webServer: externalServer
    ? undefined
    : {
        command:
          "python -m sourceloop --host 127.0.0.1 --port 8766 --data-dir runtime/e2e",
        url: "http://127.0.0.1:8766/api/health",
        timeout: 120_000,
        reuseExistingServer: false,
        stdout: "pipe",
        stderr: "pipe"
      }
});
