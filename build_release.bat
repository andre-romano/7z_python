@echo off
call .\activate.bat
call .\build_ui.bat

powershell.exe -ExecutionPolicy Bypass -File .\clean.ps1

pyinstaller ^
    --upx-dir .\upx\win ^
    --upx-exclude python3.dll ^
    --upx-exclude 7-zip32.dll ^
    --exclude-module xml ^
    --exclude-module xml.parsers ^
    --exclude-module lzma ^
    --exclude-module gzip ^
    --exclude-module bz2 ^
    --exclude-module tarfile ^
    --exclude-module zipfile ^
    --exclude-module zlib ^
    --exclude-module email ^
    --exclude-module email.message ^
    --exclude-module http ^
    --exclude-module ssl ^
    --exclude-module ftplib ^
    --exclude-module urllib ^
    --exclude-module urllib.parse ^
    --icon=".\data\icon.ico" ^
    --add-data data:data ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --optimize 1 ^
    --noconsole ^
    .\src\7z_python.py 