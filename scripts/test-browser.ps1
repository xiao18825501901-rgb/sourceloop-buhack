$ErrorActionPreference = "Stop"

$project = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $project "runtime\e2e"
$evidence = Join-Path $project "evidence"
$stdoutLog = Join-Path $runtime "server.stdout.log"
$stderrLog = Join-Path $runtime "server.stderr.log"
$transcript = Join-Path $evidence "TEST_RESULTS_PLAYWRIGHT.txt"

New-Item -ItemType Directory -Force -Path $runtime, $evidence | Out-Null

$existing = Get-NetTCPConnection -LocalPort 8766 -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    throw "Port 8766 is already in use. Stop that process before running browser tests."
}

$python = (Get-Command python -ErrorAction Stop).Source
$server = Start-Process `
    -FilePath $python `
    -ArgumentList @(
        "-m", "sourceloop",
        "--host", "127.0.0.1",
        "--port", "8766",
        "--data-dir", "runtime/e2e"
    ) `
    -WorkingDirectory $project `
    -WindowStyle Hidden `
    -PassThru `
    -RedirectStandardOutput $stdoutLog `
    -RedirectStandardError $stderrLog

$exitCode = 1
try {
    $ready = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        try {
            $response = Invoke-WebRequest `
                -UseBasicParsing `
                -Uri "http://127.0.0.1:8766/api/health" `
                -TimeoutSec 2
            if ($response.StatusCode -eq 200) {
                $ready = $true
                break
            }
        } catch {
            Start-Sleep -Milliseconds 250
        }
    }
    if (-not $ready) {
        throw "The local test server did not become ready. See $stderrLog"
    }

    $env:SOURCELOOP_EXTERNAL_SERVER = "1"
    $ErrorActionPreference = "Continue"
    "SourceLoop browser acceptance run - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')" |
        Set-Content -LiteralPath $transcript -Encoding utf8
    & npx playwright test @args 2>&1 |
        Tee-Object -FilePath $transcript -Append
    $exitCode = $LASTEXITCODE
} finally {
    Remove-Item Env:SOURCELOOP_EXTERNAL_SERVER -ErrorAction SilentlyContinue
    if (-not $server.HasExited) {
        Stop-Process -Id $server.Id -Force
        $server.WaitForExit()
    }
}

exit $exitCode
