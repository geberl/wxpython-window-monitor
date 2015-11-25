@echo off

REM  Show start time of script.
echo Started building at %date%, %time%

REM Change to parent directory of this one.
cd "%~dp0"
cd ..

REM  Run PyInstaller (latest version from GitHub, not the version from PyPi) with parameters in spec file.
C:\Python\Scripts\pyinstaller.exe --clean --upx-dir=C:\00_Privat\20_USB\upx\ setup_pyinstaller_onefile.spec

REM  Show end time of script.
echo Building finished at %date%, %time%

REM  Newline.
echo.

REM  Wait for user key press to close window.
pause
