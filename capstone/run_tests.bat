@echo off
cd /d "%~dp0"
echo ========================================================
echo       Running Assembler Test Suite (compare.py)
echo ========================================================
call python.bat compare.py
echo.
pause
