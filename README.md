# 7z Python

Frontend GUI tool to manage 7zip SFX with an easy to use interface, supporting autorun scripts (executed after decompression).

**Summary**:
- [7z Python](#7z-python)
  - [How to create an SFX with autorun script](#how-to-create-an-sfx-with-autorun-script)
    - [Examples](#examples)
  - [Building (Windows .exe)](#building-windows-exe)
  - [Download stable releases (binary EXE files)](#download-stable-releases-binary-exe-files)
  - [Special thanks / Acknowledgments](#special-thanks--acknowledgments)
  - [License and Copyright](#license-and-copyright)


## How to create an SFX with autorun script

1. Open the 7z Python
2. Select files to compress
3. Create a ``7z_python.ini`` file with the following INI sections
   ```ini
   [SFX]   
   autorun=command_to_execute_after_decompression
   input_file=input_compressed_file_to_extract
   output_path=destination_path_for_files
   silent=0_or_1_here
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

- **silent**: describes if the SFX should run silently (without user interaction) or not
  - E.g.: 0 (non silent SFX)
  - E.g.: 1 (silent SFX -- no user input will be requested)

### Examples

You can find examples on how to create a config .INI file in the path [./examples](./examples/) of this repository.

## Building (Windows .exe)

Run the following within the CMD prompt terminal:
```batch
call ".\install_dependencies.bat"
call ".\build_release.bat"
```

## Download stable releases (binary EXE files)

Check the [Releases](https://github.com/andre-romano/7z_python/releases/) pages (right side of this page).

## Special thanks / Acknowledgments

- [Qt6](https://www.qt.io/)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [7zip project](https://www.7-zip.org/)
- [Flaticon](https://www.flaticon.com/)

## License and Copyright

Copyright (C) [2025] Andre Luiz Romano Madureira

This project is licensed under the GNU Lesser General Public License (LGPL).  
You are free to use, modify, and distribute this software under the terms of the LGPL.

For more details, see the full license text (see [./LICENSE](./LICENSE) file).

You can also see the the full license text here:
[GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.html)