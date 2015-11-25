@echo off

REM  Show start time of script.
echo Started cleanup at %date%, %time%

REM Change to parent directory of this one.
cd "%~dp0"
cd ..

REM  Remove all *.pyc and *.pyo files.
del *.pyc /s /F /Q
del *.pyo /s /F /Q

REM  Remove build and dist folders including subfolders and files.
rd build /s /q
rd dist /s /q

REM Remove __pycache__ folder including subfolders and files.
rd __pycache__ /s /q

REM  Show end time of script.
echo Cleanup finished at %date%, %time%

REM  Newline.
echo.

REM  Wait for user key press to close window.
pause
