@echo off
REM Change to the directory of the CMD script
cd /d "%~dp0"

REM Run the Python script
python rename-scores.py

REM Pause to keep the command prompt window open
pause
