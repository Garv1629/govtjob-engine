@echo off
title GovtJob Backend Engine
echo ===================================================
echo   GovtJob AI Agent - Backend Engine Auto-Setup
echo ===================================================
cd /d "%~dp0"

:: 1. If uvicorn is missing, purge broken venv unconditionally
if not exist "%~dp0venv\Scripts\uvicorn.exe" (
    echo [*] Purging broken/incomplete virtual environment...
    if exist "%~dp0venv" rmdir /s /q "%~dp0venv"
)

:: 2. Ensure stable Python 3.12 is installed if py launcher lacks it
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    py -3.11 --version >nul 2>&1
    if errorlevel 1 (
        echo [*] Installing official stable Python 3.12...
        winget install 9NCVDN91XZQP --accept-package-agreements --accept-source-agreements
    )
)

:: 3. Create fresh venv using py launcher
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [*] Creating Python Virtual Environment...
    py -3.12 -m venv venv 2>nul
    if not exist venv py -3.11 -m venv venv 2>nul
    if not exist venv py -3.10 -m venv venv 2>nul
    if not exist venv py -3 -m venv venv 2>nul
    if not exist venv python -m venv venv
)

echo [*] Activating Virtual Environment...
call "%~dp0venv\Scripts\activate.bat"

:: 4. Direct PIP installation
if not exist "%~dp0venv\Scripts\uvicorn.exe" (
    echo [*] Installing backend dependencies...
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic apscheduler openai python-telegram-bot httpx python-multipart passlib cryptography
)

echo.
echo ===================================================
echo   Starting Backend Server on http://localhost:8000
echo ===================================================
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
pause
