import os
import logging

from PyQt6.QtWidgets import QWidget, QFileDialog

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class FileDialog:
    @staticmethod
    def _fixPathSeparator(filename: str):
        filename = filename.replace('/', os.path.sep)
        filename = filename.replace('\\', os.path.sep)
        return filename

    def __init__(self, parent: QWidget = None):
        self.parent = parent

    def selectFiles(self, title: str, err_msg: str, filter: str = None):
        """
        Function to select multiple files using QFileDialog.
        :param filter: Filter for file types.
        :return: List of selected files or None if no files were selected.

        :raise Exception if no files selected
        """
        logger.info(f"(title={title}, filter={filter})")
        files, _ = QFileDialog.getOpenFileNames(
            self.parent, title, filter=filter)
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
        file, _ = QFileDialog.getOpenFileName(
            self.parent, title, filter=filter)
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
        directory = QFileDialog.getExistingDirectory(
            self.parent, title)
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
        file, _ = QFileDialog.getSaveFileName(
            self.parent, title, filter=filter)
        if not file:
            raise Exception(err_msg)

        file = self._fixPathSeparator(file)

        logger.info(f"{file}")
        return file
