# 7z Python

Frontend GUI tool to manage 7zip SFX with an easy to use interface, supporting autorun script files (autorun.inf, autorun.ps1, autorun.bat, autorun.py).

## How to create an SFX with autorun script

1. Open the 7z Python
2. Select files to compress using 7z console
3. Include an autorun script (autorun.inf, autorun.ps1, autorun.bat, or autorun.py)
4. Whatever instructions present in the autorun script will be read and executed by 7z Python after data decompression

**PS:** 7z Python uses 7z file split (default 650 MB files) to facilitate data distribution. This can be changed by modifying **PARAM** key in `data\config.INI` and rebuilding 7z Python.

## Building (Windows .exe)

Run the following within the CMD prompt terminal:
```batch
call ".\install_dependencies.bat"
call ".\build_release.bat"
```

## Building (Installer -- InnoSetup)

Build the InnoSetup scripts (`.ISS` files) to create the installable version of the software.

## Stable Releases

Check the Releases pages in GitHub (on the right side of this page).

## Special thanks / Acknowledgments

- [7zip project](https://www.7-zip.org/)
- [Flaticon](https://www.flaticon.com/)
- [PyQt5](https://pypi.org/project/PyQt5/)

## Copyright

Copyright (C) [2024] Andre Luiz Romano Madureira

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program (see [./LICENSE](./LICENSE) file). If not, see <https://www.gnu.org/licenses/>.