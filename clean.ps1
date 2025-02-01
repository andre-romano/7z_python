# pyinstaller --clean main.py
Remove-Item -Path ".\build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item *.spec -ErrorAction SilentlyContinue