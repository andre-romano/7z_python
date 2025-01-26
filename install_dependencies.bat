@echo off
call .\activate.bat

pip install -r requirements.txt
pip freeze > .\requirements.txt
