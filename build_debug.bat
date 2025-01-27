@echo off
call .\activate.bat

powershell.exe -ExecutionPolicy Bypass -File .\clean.ps1

pyinstaller --icon=".\data\icon.ico" --add-data data:data --onefile .\src\7z_python.py
