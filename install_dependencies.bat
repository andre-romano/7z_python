@echo off
call .\activate.bat

echo Upgrading pip, setuptools, wheel ...
pip3 install --upgrade pip setuptools wheel

if exist .\requirements.lock (
    echo File requirements.lock found, installing dependencies...
    pip3 install -r .\requirements.lock --prefer-binary --no-cache-dir
) else if exist .\requirements.txt (
    echo File requirements.lock NOT found, installing dependencies from requirements.txt ...
    pip3 install -r requirements.txt --prefer-binary --no-cache-dir
)
echo Freezing depedencies in requirements.lock ...
pip3 freeze > .\requirements.lock
