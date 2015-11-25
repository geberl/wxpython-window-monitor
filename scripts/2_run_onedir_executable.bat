@echo off

REM  Show start time of script.
echo Started executable at %date%, %time%

REM Change to parent directory of this one.
cd "%~dp0"
cd ..

REM Change to dist/main directory.
cd dist
cd main

REM  Run executable.
winmon.exe

REM  Show end time of script.
echo Executable quit at %date%, %time%

REM  Newline.
echo.

REM  Wait for user key press to close window.
pause
