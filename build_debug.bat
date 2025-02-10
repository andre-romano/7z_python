@echo off
call .\activate.bat
call .\build_ui.bat

powershell.exe -ExecutionPolicy Bypass -File .\clean.ps1

pyinstaller ^
    --upx-dir .\upx\win ^
    --upx-exclude python3.dll ^
    --upx-exclude 7-zip32.dll ^
    --icon=".\data\icon.ico" ^
    --add-data data:data ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --debug all ^
    .\src\_main.py

