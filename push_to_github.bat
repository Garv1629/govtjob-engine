@echo off
cd /d "%~dp0"
if not exist ".git" (
    echo Initializing Git repository...
    git init
)
echo Staging and committing latest changes...
git add .
git commit -m "Fix Telegram bot poller, DB sessions, browser manager syntax, and website backend integration"
git branch -M main
git remote add origin https://github.com/Garv1629/govtjob-engine.git 2>nul
git remote set-url origin https://github.com/Garv1629/govtjob-engine.git 2>nul
echo Pushing code to GitHub repository (https://github.com/Garv1629/govtjob-engine.git)...
git push -u origin main --force
echo Done! Pushed latest updates successfully.
pause
