#!/bin/python3
import logging
import sys
import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QMessageBox, QProgressBar

from Config import Config
from Localization import Localization

from Regex import Regex
from FileDialog import FileDialog
from SevenZip import SevenZip

# Create a logger for this module
logger = logging.getLogger(__name__)


class MainWindow(QWidget):
    def __init__(self, data_path, debug=False):
        super().__init__()
        logger.info(f"(data_path={data_path}, debug={debug})")

        self.env = os.environ.copy()
        self.env['LANG'] = os.getenv('LANG', 'en').split('_')[0].split('-')[0]

        logger.debug(f"env['LANG']={self.env['LANG']}")

        self.paths = {
            'data_path': data_path,
            'locale_path': f"{data_path}{os.path.sep}lang",
            'config_file': f"{data_path}{os.path.sep}config.ini"
        }

        self.config = Config(self.paths['config_file'])
        self.sevenZip = SevenZip(
            data_path=self.paths['data_path'],
            start_callback=self.on_started,
            update_callback=self.on_update,
            finish_callback=self.on_finish
        )
        self.localization = Localization(
            locale_dir=self.paths['locale_path'],
            lang=self.env['LANG'],
            default_lang='en'
        )

        self.setWindowTitle("7-Zip Python Frontend")
        self.setGeometry(300, 300, 600, 400)
        self.setLayout(self._init_UI())

    def _init_UI(self) -> QLayout:
        loc = self.localization
        layout = QVBoxLayout()

        label_txt = loc.translate("Main.operation_label")
        self.label = QLabel(label_txt)
        layout.addWidget(self.label)

        compress_btn_txt = loc.translate("Main.compress_btn")
        self.compress_button = QPushButton(compress_btn_txt)
        self.compress_button.clicked.connect(self.compress_files)
        layout.addWidget(self.compress_button)

        decompress_btn_txt = loc.translate("Main.decompress_btn")
        self.decompress_button = QPushButton(decompress_btn_txt)
        self.decompress_button.clicked.connect(self.decompress_files)
        layout.addWidget(self.decompress_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        return layout

    def compress_files(self):
        loc = self.localization
        try:
            input_files_txt = loc.translate("CompressDialog.input_files")
            input_err_txt = loc.translate("CompressDialog.input_err")
            files = FileDialog(input_files_txt, self).selectFiles(
                err_msg=input_err_txt)

            out_file_txt = loc.translate("CompressDialog.output_file")
            out_err_txt = loc.translate("CompressDialog.output_err")
            out_filter_txt = loc.translate("CompressDialog.output_file_filter")
            output_file = FileDialog(out_file_txt, self).selectSaveFile(
                err_msg=out_err_txt,
                filter=out_filter_txt)

            extra_args = self.config.get('Compression.extra_args', '').split()
            command = ["a"] + extra_args
            command += [output_file] + files
            self.sevenZip.start(command)
        except Exception as e:
            logger.error(f"{e}")
            QMessageBox.critical(
                self, f"Error", f"{e}")

    def decompress_files(self):
        loc = self.localization
        try:
            input_files_txt = loc.translate(
                "DecompressDialog.input_file")
            input_err_txt = loc.translate(
                "DecompressDialog.input_err")
            input_filter_txt = loc.translate(
                "DecompressDialog.input_file_filter")
            archive_file = FileDialog(input_files_txt, self).selectFile(err_msg=input_err_txt,
                                                                        filter=input_filter_txt)

            out_dir_txt = loc.translate(
                "DecompressDialog.output_dir")
            out_err_txt = loc.translate(
                "DecompressDialog.output_err")
            output_dir = FileDialog(
                out_dir_txt, self).selectDirectory(err_msg=out_err_txt)

            extra_args = self.config.get(
                'Decompression.extra_args', '').split()
            command = ["x", archive_file]
            command += [f"-o{output_dir}"]
            command += extra_args
            self.sevenZip.start(command)
        except Exception as e:
            logger.error(f"{e}")
            QMessageBox.critical(
                self, f"Error", f"{e}")

    def on_started(self):
        self.log_output.clear()
        self.progress_bar.setValue(0)

    def on_update(self, message: str):
        # logger.debug(message)
        self.log_output.append(message)
        self.update_progress(message)
        self.check_return_code(message)

    def on_finish(self):
        self.progress_bar.setValue(100)

    def update_progress(self, message):
        try:
            # Search for progress percentage in the message using the regex pattern
            # (e.g., "Extracting: 23%")
            regex = Regex(r"(Compressing|Extracting).*\s(\d+)%")
            match = regex.search(message)
            # Extract percentage
            operation, percentage = match.groups()
            percentage = int(percentage)
            # Update the progress bar value
            self.progress_bar.setValue(percentage)
        except Exception as e:
            pass

    def check_return_code(self, message):
        loc = self.localization
        msg_box_title = loc.translate("OpFinish_MsgBox.title")
        msg_box_succ = loc.translate("OpFinish_MsgBox.content_succ")
        msg_box_fail = loc.translate("OpFinish_MsgBox.content_fail")
        try:
            # Pattern (e.g., "Return code: 0")
            regex = Regex(r"Return code:.*(\d+)")
            match = regex.search(message)
            # Extract percentage
            retcode = int(match.groups()[0])
            # Update the progress bar value
            if retcode == 0:
                QMessageBox.information(
                    self, msg_box_title, msg_box_succ)
            else:
                QMessageBox.critical(
                    self, msg_box_title, msg_box_fail)
        except Exception as e:
            pass
