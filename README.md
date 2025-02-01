# 7z Python

Frontend GUI tool to manage 7zip SFX with an easy to use interface, supporting autorun scripts (executed after decompression).

**Summary**:
- [7z Python](#7z-python)
  - [How to create an SFX with autorun script](#how-to-create-an-sfx-with-autorun-script)
  - [Building (Windows .exe)](#building-windows-exe)
  - [Stable Releases](#stable-releases)
  - [Special thanks / Acknowledgments](#special-thanks--acknowledgments)
  - [Copyright](#copyright)


## How to create an SFX with autorun script

1. Open the 7z Python
2. Select files to compress
3. Create a ``7z_python.ini`` file with the following INI sections
   ```ini
   [SFX]   
   autorun=command_to_execute_after_decompression
   input_file=input_compressed_file_to_extract
   output_path=destination_path_for_files
   ```

**SFX OPTIONS**:

- **autorun**: describes a command to run after file decompression
  - E.g.: powershell.exe -ExecutionPolicy Bypass -File "setup.ps1"
  - E.g.: cmd.exe /c script.bat
  - E.g.: my_program.exe

- **input_file**: describes which file to decompress
  - E.g.: my_file.7z
  - E.g.: zipped_content.zip
  - E.g.: file.gz

- **output_path**: describes the path to decompress the files
  - E.g.: C:\Users\John\Downloads
  - E.g.: C:\ProgramFiles\

## Building (Windows .exe)

Run the following within the CMD prompt terminal:
```batch
call ".\install_dependencies.bat"
call ".\build_release.bat"
```

## Stable Releases

Check the [Releases](./releases/) pages in GitHub (on the right side of this page).

## Special thanks / Acknowledgments

- [7zip project](https://www.7-zip.org/)
- [Flaticon](https://www.flaticon.com/)
- [PyQt5](https://pypi.org/project/PyQt5/)

## Copyright

Copyright (C) [2025] Andre Luiz Romano Madureira

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program (see [./LICENSE](./LICENSE) file). If not, see <https://www.gnu.org/licenses/>.