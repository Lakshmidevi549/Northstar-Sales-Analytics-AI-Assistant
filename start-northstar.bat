@echo off
cd /d "%~dp0"
python 04_AI_Dashboard\app.py
if errorlevel 1 (
  echo.
  echo Northstar stopped. Check that Python and data\northstar.db are available.
)
pause
