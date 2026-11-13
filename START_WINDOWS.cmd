@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1

where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 or newer is required but was not found on PATH.
  pause
  exit /b 1
)

echo Starting SourceLoop at http://127.0.0.1:8765/
python -m sourceloop --host 127.0.0.1 --port 8765 --open

if errorlevel 1 (
  echo.
  echo SourceLoop stopped with an error.
  pause
)
