# Exemples

This folder provides examples of 7z_python usage and configuration.

### SFX -- NO Autorun file

- **[./sfx_no_autorun/](./sfx_no_autorun/)**
  - User is prompted for decompression confirmation.
  - Extracts the contents of the compressed file automatically, to the current working directory (e.g., `pwd`).
- **[./sfx_no_autorun_silent/](./sfx_no_autorun_silent/)**
  - NO USER PROMPT is requested (**silent operation**).
  - Extracts the contents of the compressed file automatically, to the current working directory (e.g., `pwd`).

### SFX -- WITH Autorun file
- **[./sfx_with_autorun/](./sfx_with_autorun/)**
  - User is prompted for decompression confirmation.
  - Extracts the contents of the compressed file automatically, to the current working directory.
  - Runs ``autorun.ps1`` file automatically, after decompression
- **[./sfx_with_autorun_silent/](./sfx_with_autorun_silent/)**
  - NO USER PROMPT is requested (**silent operation**).
  - Extracts the contents of the compressed file automatically, to the current working directory.
  - Runs ``autorun.ps1`` file automatically, after decompression