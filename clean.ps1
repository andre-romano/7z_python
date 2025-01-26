# pyinstaller --clean main.py
Remove-Item -Path ".\build" -Recurse -Force
Remove-Item -Path ".\dist" -Recurse -Force
Remove-Item *.spec