@echo off
call .\activate.bat

powershell.exe -ExecutionPolicy Bypass -File .\clean.ps1

pyinstaller --icon=".\data\icon.ico" --add-data data:data --onefile --upx-dir .\upx\win --upx-exclude python3.dll --upx-exclude 7-zip32.dll --clean .\src\7z_python.py

