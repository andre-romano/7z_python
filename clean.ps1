# pyinstaller --clean main.py

$folders = @(".\build", ".\dist")
foreach ($folder in $folders) {
    Remove-Item -Path "$folder" -Recurse -Force -ErrorAction SilentlyContinue
}

$extensions = @(
    "spec", "log", 
    "7z", "zip", "rar", "lzma", "lzma2", 
    "gzip", "bz2", "xz",
    "tar.gz", "tar.bz2", "tar.xz", "tar"    
)
foreach ($ext in $extensions) {
    Remove-Item "*.$ext" -ErrorAction SilentlyContinue
}
