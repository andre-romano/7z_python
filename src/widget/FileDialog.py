import os
import logging

from tkinter import filedialog

from Regex import Regex

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class FileDialog:

    # Assuming 'filter' is the filter string, e.g., "Arquivos comprimidos (*.7z *.zip *.rar *.gz *.xz *.bz2 *.tar *.tar.gz *.tar.xz *.tar.bz2)"
    @staticmethod
    def _decode_filetypes(filters: str) -> list:
        # Use a regular expression to extract the description and file extensions
        if not filters:
            return [('All', tuple(['*.*']))]
        return [
            (
                ft.split("(")[0].strip(),
                tuple(ft.split("(")[1].replace(")", '').split())
            )
            for ft in filters.split("||")
        ]

    @staticmethod
    def _fixPathSeparator(filename: str):
        filename = filename.replace('/', os.path.sep)
        filename = filename.replace('\\', os.path.sep)
        return filename

    def __init__(self):
        pass

    def selectFiles(self, title: str, err_msg: str, filter: str = None):
        """
        Function to select multiple files using QFileDialog.
        :param filter: Filter for file types.
        :return: List of selected files or None if no files were selected.

        :raise Exception if no files selected
        """
        logger.info(f"(title={title}, filter={filter})")
        files = filedialog.askopenfilenames(
            title=title,
            filetypes=self._decode_filetypes(filter)
        )
        if not files:
            raise Exception(err_msg)

        files = list(map(self._fixPathSeparator, files))

        logger.info(f"{files}")
        return files

    def selectFile(self, title: str, err_msg: str, filter: str = None):
        """
        Function to select a single file using QFileDialog.
        :param filter: Filter for file types.
        :return: Selected file path or None if no file was selected.
        """
        logger.info(f"(title={title}, filter={filter})")
        file = filedialog.askopenfilename(
            title=title,
            filetypes=self._decode_filetypes(filter)
        )
        if not file:
            raise Exception(err_msg)

        file = self._fixPathSeparator(file)

        logger.info(f"{file}")
        return file

    def selectDirectory(self, title: str, err_msg: str):
        """
        Function to select a directory using QFileDialog.
        :return: Selected directory or None if no directory was selected.
        """
        logger.info(f"(title={title})")
        directory = filedialog.askdirectory(title=title)
        if not directory:
            raise Exception(err_msg)

        directory = self._fixPathSeparator(directory)

        logger.info(f"{directory}")
        return directory

    def selectSaveFile(self, title: str, err_msg: str, filter: str = None):
        """
        Function to select an save file (with save option) using QFileDialog.
        :param filter: Filter for file types.
        :return: Save file path or None if no file was selected.
        """
        logger.info(f"(title={title}, filter={filter})")
        filetypes = self._decode_filetypes(filter)
        file = filedialog.asksaveasfilename(
            title=title,
            filetypes=filetypes,
            defaultextension=filetypes[0][1]
        )
        if not file:
            raise Exception(err_msg)

        file = self._fixPathSeparator(file)

        logger.info(f"{file}")
        return file
