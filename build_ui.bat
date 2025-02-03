@echo off
call .\activate.bat

set "UI_FOLDER_SRC=src\ui"
set "UI_FOLDER_DST=src\ui"

REM Enable delayed variable expansion
setlocal enabledelayedexpansion

REM Loop through all files in the source folder
for %%i in ("%UI_FOLDER_SRC%\*") do (
    REM Check if the file is a .ui file
    if "%%~xi"==".ui" (
        REM Extract the filename without extension
        set "FILENAME=%%~ni"
        
        REM Convert .ui to .py using pyuic6
        echo Building UI file %%i ...
        pyuic6 -o "%UI_FOLDER_DST%\!FILENAME!.py" "%%i"
    )
)

REM End delayed expansion
endlocal
echo Building UI - FINISHED
