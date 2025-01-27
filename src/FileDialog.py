import os
import logging

from PyQt5.QtWidgets import QWidget, QFileDialog

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class FileDialog:
    @staticmethod
    def _fixPathSeparator(filename: str):
        filename = filename.replace('/', os.path.sep)
        filename = filename.replace('\\', os.path.sep)
        return filename

    def __init__(self, dialog_title: str, parent: QWidget = None):
        self.dialog_title = dialog_title
        self.parent = parent

    def selectFiles(self, err_msg: str, filter: str = None):
        """
        Function to select multiple files using QFileDialog.
        :param filter: Filter for file types.
        :return: List of selected files or None if no files were selected.

        :raise Exception if no files selected
        """
        logger.info(f"(dialog={self.dialog_title}, filter={filter})")
        files, _ = QFileDialog.getOpenFileNames(
            self.parent, self.dialog_title, filter=filter)
        if not files:
            raise Exception(err_msg)

        files = list(map(self._fixPathSeparator, files))

        logger.info(f"{files}")
        return files

    def selectFile(self, err_msg: str, filter: str = None):
        """
        Function to select a single file using QFileDialog.
        :param filter: Filter for file types.
        :return: Selected file path or None if no file was selected.
        """
        logger.info(f"(dialog={self.dialog_title}, filter={filter})")
        file, _ = QFileDialog.getOpenFileName(
            self.parent, self.dialog_title, filter=filter)
        if not file:
            raise Exception(err_msg)

        file = self._fixPathSeparator(file)

        logger.info(f"{file}")
        return file

    def selectDirectory(self, err_msg: str):
        """
        Function to select a directory using QFileDialog.
        :return: Selected directory or None if no directory was selected.
        """
        logger.info(f"(dialog={self.dialog_title})")
        directory = QFileDialog.getExistingDirectory(
            self.parent, self.dialog_title)
        if not directory:
            raise Exception(err_msg)

        directory = self._fixPathSeparator(directory)

        logger.info(f"{directory}")
        return directory

    def selectSaveFile(self, err_msg: str, filter: str = None):
        """
        Function to select an save file (with save option) using QFileDialog.
        :param filter: Filter for file types.
        :return: Save file path or None if no file was selected.
        """
        logger.info(f"(dialog={self.dialog_title}, filter={filter})")
        file, _ = QFileDialog.getSaveFileName(
            self.parent, self.dialog_title, filter=filter)
        if not file:
            raise Exception(err_msg)

        file = self._fixPathSeparator(file)

        logger.info(f"{file}")
        return file
