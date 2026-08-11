@echo off
title GovtJob AI Agent - All-in-One Engine
echo ===================================================
echo   GovtJob AI Agent - Single Window Master Launcher
echo ===================================================
echo.
echo Launching Backend (Port 8000) & Frontend (Port 3000) in THIS single window...
echo.

:: Launch Backend in SAME window
start /b cmd /c "cd /d %~dp0backend && run_backend.bat"

:: Launch Frontend in SAME window
start /b cmd /c "cd /d %~dp0frontend && run_frontend.bat"

echo.
echo ===================================================
echo   Both Services active in this single terminal!
echo   Opening Website in Browser...
echo ===================================================
echo.

timeout /t 5 > nul
start http://localhost:3000

:: Keep master terminal open
cmd /k
