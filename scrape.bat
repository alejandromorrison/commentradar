@echo off
REM Quick scraper for Windows
REM Usage: scrape.bat "your topic"

REM Create scrape folder if it doesn't exist
if not exist "scrape" mkdir scrape

if "%~1"=="" (
    echo.
    echo ================================================================
    echo                    CommentRadar Quick Scraper
    echo ================================================================
    echo.
    echo Usage: scrape.bat "your topic"
    echo.
    echo Examples:
    echo   scrape.bat "AI tools"
    echo   scrape.bat "fitness apps"
    echo   scrape.bat "meal planning software"
    echo.
    set /p topic="Enter topic to scrape: "
) else (
    set topic=%~1
)

echo.
echo Scraping: %topic%
echo All results will be saved in the 'scrape' folder
echo.

python quick_scrape.py "%topic%"

echo.
echo Check the 'scrape' folder for your results!
echo.

pause

