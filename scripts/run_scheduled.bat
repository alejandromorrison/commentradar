@echo off
REM Windows batch script to run scheduled scraping
REM Usage: run_scheduled.bat

echo Starting CommentRadar Scheduler...
echo This will run every 30 minutes.
echo Press Ctrl+C to stop.
echo.

cd /d "%~dp0.."
python -m commentradar.scheduler --topic "tech news" --interval 30 --limit 50 --analyze-sentiment

pause

