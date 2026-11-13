$ErrorActionPreference = "Stop"

$project = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $project "runtime\demo"
$evidence = Join-Path $project "evidence"
$stdoutLog = Join-Path $runtime "server.stdout.log"
$stderrLog = Join-Path $runtime "server.stderr.log"
$narration = Join-Path $evidence "demo-narration.wav"
$rawVideo = Join-Path $evidence "SourceLoop-demo-raw.webm"
$finalVideo = Join-Path $evidence "SourceLoop-demo.mp4"

New-Item -ItemType Directory -Force -Path $runtime, $evidence | Out-Null

$existing = Get-NetTCPConnection -LocalPort 8767 -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    throw "Port 8767 is already in use. Stop that process before recording."
}

& (Join-Path $PSScriptRoot "make-demo-narration.ps1") | Out-Null

$audioSeconds = [double](& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $narration)
$targetSeconds = [Math]::Min(170, [Math]::Max(148, [Math]::Ceiling($audioSeconds + 7)))

$python = (Get-Command python -ErrorAction Stop).Source
$server = Start-Process `
    -FilePath $python `
    -ArgumentList @(
        "-m", "sourceloop",
        "--host", "127.0.0.1",
        "--port", "8767",
        "--data-dir", "runtime/demo"
    ) `
    -WorkingDirectory $project `
    -WindowStyle Hidden `
    -PassThru `
    -RedirectStandardOutput $stdoutLog `
    -RedirectStandardError $stderrLog

try {
    $ready = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        try {
            $response = Invoke-WebRequest `
                -UseBasicParsing `
                -Uri "http://127.0.0.1:8767/api/health" `
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
        throw "The demo server did not become ready. See $stderrLog"
    }

    $env:SOURCELOOP_DEMO_URL = "http://127.0.0.1:8767"
    $env:SOURCELOOP_DEMO_TARGET_SECONDS = "$targetSeconds"
    node (Join-Path $PSScriptRoot "record-demo.js")
    if ($LASTEXITCODE -ne 0) {
        throw "The Playwright recorder failed."
    }
} finally {
    Remove-Item Env:SOURCELOOP_DEMO_URL -ErrorAction SilentlyContinue
    Remove-Item Env:SOURCELOOP_DEMO_TARGET_SECONDS -ErrorAction SilentlyContinue
    if (-not $server.HasExited) {
        Stop-Process -Id $server.Id -Force
        $server.WaitForExit()
    }
}

if (-not (Test-Path -LiteralPath $rawVideo)) {
    throw "The raw demo video was not created."
}

$videoSeconds = [double](& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $rawVideo)
$outputSeconds = [Math]::Min(165, [Math]::Max(145, [Math]::Max($videoSeconds, $audioSeconds / 1.1 + 2)))

& ffmpeg `
    -y `
    -i $rawVideo `
    -i $narration `
    -filter_complex "[1:a]adelay=800|800,atempo=1.1,apad=whole_dur=$outputSeconds[a]" `
    -map 0:v `
    -map "[a]" `
    -c:v libx264 `
    -preset medium `
    -crf 23 `
    -pix_fmt yuv420p `
    -c:a aac `
    -b:a 160k `
    -movflags +faststart `
    -t $outputSeconds `
    $finalVideo

if ($LASTEXITCODE -ne 0) {
    throw "ffmpeg failed to produce the demo MP4."
}

Write-Output $finalVideo
