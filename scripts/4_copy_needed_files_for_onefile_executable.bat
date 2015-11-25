@echo off

REM  Show start time of script.
echo Started copying at %date%, %time%

REM Change to parent directory of this one.
cd "%~dp0"
cd ..

REM Copy files.
xcopy "icon.ico" "dist" /Y
xcopy "logging_to_file.ini" "dist" /Y
xcopy "settings.ini" "dist" /Y

REM  Show end time of script.
echo Copying finished at %date%, %time%

REM  Newline.
echo .

REM  Wait for user key press to close window.
pause
