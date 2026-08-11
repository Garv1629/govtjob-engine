@echo off
title GovtJob Frontend App
echo ===================================================
echo   GovtJob AI Agent - Frontend App Auto-Setup
echo ===================================================
cd /d "%~dp0"

if not exist "%~dp0node_modules" (
    echo Installing NPM Packages (This happens only on first run)...
    call npm install
)

echo.
echo ===================================================
echo   Starting Next.js Server on http://localhost:3000
echo ===================================================
call npm run dev
pause
