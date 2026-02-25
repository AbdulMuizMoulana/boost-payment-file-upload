@echo off

echo ============================================
echo      BOOST FILE UPLOAD AUTOMATION BOT
echo ============================================

REM ---- Go to project directory ----
cd /d %~dp0

REM ---- Activate virtual environment ----
call .venv\Scripts\activate

REM ---- Set environment variables ----
set HEADLESS=true
set BROWSER=chrome

REM ---- Screen size for headless ----
set WINDOW_WIDTH=1920
set WINDOW_HEIGHT=1080

REM ---- Run tests (DEV only) ----
pytest -v

if %ERRORLEVEL% EQU 0 (
    echo ============================================
    echo        EXECUTION COMPLETED
    echo ============================================
    echo SUCCESS
) else (
    echo FAILED
)

pause
