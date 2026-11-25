@echo off
cd /d "%~dp0"
echo ========================================================
echo       Assembling Box.asm using assembler.py
echo ========================================================
call python.bat assembler.py Box.asm
echo.
echo Assembled Box.hack and updated symbols.txt successfully!
echo ========================================================
pause
