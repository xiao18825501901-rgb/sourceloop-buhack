$ErrorActionPreference = "Stop"

$project = Split-Path -Parent $PSScriptRoot
$evidence = Join-Path $project "evidence"
$output = Join-Path $evidence "demo-narration.wav"

New-Item -ItemType Directory -Force -Path $evidence | Out-Null

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $synth.SelectVoice("Microsoft Zira Desktop")
} catch {
    throw "Microsoft Zira Desktop is not available for the demo narration."
}

$synth.Rate = -2
$synth.Volume = 100

$narration = @"
Students do not need another pile of notes. When a question goes wrong, they need the exact sentence they missed.

SourceLoop makes that return path part of the study loop.

Here is the first lesson in the original Campus Routes Lab course. The explanation says that a weighted graph is a set of places and costs. Click the source chip, and the exact passage opens beside the lesson. The claim and the evidence stay connected.

Now switch to Chinese. The course, the source desk, the practice, and the controls all follow the language choice. This is not a translated screenshot. The content is rendered from the same bilingual pack.

The frontier lesson contains a real Dijkstra computation. The local server records each settlement, each tentative distance, and each edge relaxation. Step forward and watch the frontier change. Library to Canteen to Lab is the shortest route, with total cost nine. We did not record the answer. We exposed the computation that produced it.

Practice is graded by the local server. The browser does not receive the answer key before submission. A wrong choice returns the result, the reasoning, and a direct link to the source. It also creates one deduplicated review item, so a learner has a clear next action instead of a vague score.

Retrying correctly resolves that same review item. The learner can continue without carrying duplicate mistakes.

The third lesson makes the assumption visible. Dijkstra is safe here because every edge has a non-negative weight. That is a teaching boundary, not hidden implementation detail.

Students can also bring their own Markdown or plain-text notes. The import flow creates literal quote and source-location checks. It does not invent a new explanation and does not replace the student's notes as the source of truth.

Finally, export the pack. The result is one self-contained HTML file. Here it is opened over file, with the browser offline. The graph still runs, the language control still works, and practice still grades locally. The study loop is portable.

SourceLoop. Turn your notes into a cited, interactive study loop.
"@

$synth.SetOutputToWaveFile($output)
$synth.Speak($narration)
$synth.SetOutputToNull()
$synth.Dispose()

if (-not (Test-Path -LiteralPath $output)) {
    throw "Narration was not created."
}

Write-Output $output
