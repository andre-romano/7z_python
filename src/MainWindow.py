#!/bin/python3
import logging
import sys
import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
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

        self._setENV(data_path)

        self.config = Config(self.env['CONFIG_FILE'])
        self.sevenZip = SevenZip(
            env=self.env,
            start_callback=self.on_started,
            update_callback=self.on_update,
            finish_callback=self.on_finish
        )
        self.localization = Localization(env=self.env)

        self.setWindowTitle("7-Zip Python Frontend")
        self.setGeometry(300, 300, 600, 400)
        self.setLayout(self._init_UI())

    def _setENV(self, data_path: str):
        self.env = os.environ.copy()

        # path config
        self.env['DATA_PATH'] = data_path
        self.env['LOCALE_PATH'] = f"{data_path}{os.path.sep}lang"
        self.env['CONFIG_FILE'] = f"7z_python.ini"

        # language config
        self.env['LANG_DEFAULT'] = 'en'
        self.env['LANG'] = self.env.get('LANG', self.env['LANG_DEFAULT'])
        self.env['LANG'] = self.env['LANG'].split('_')[0].split('-')[0]

    def _init_UI(self) -> QLayout:
        loc = self.localization
        layout = QVBoxLayout()

        label_txt = loc["Main.operation_label"]
        self.label = QLabel(label_txt)
        layout.addWidget(self.label)

        compress_btn_txt = loc["Main.compress_btn"]
        self.compress_button = QPushButton(compress_btn_txt)
        self.compress_button.clicked.connect(self.on_click_btn_compress)
        layout.addWidget(self.compress_button)

        decompress_btn_txt = loc["Main.decompress_btn"]
        self.decompress_button = QPushButton(decompress_btn_txt)
        self.decompress_button.clicked.connect(self.on_click_btn_decompress)
        layout.addWidget(self.decompress_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        return layout

    def on_click_btn_compress(self):
        loc = self.localization
        try:
            input_files_txt = loc["CompressDialog.input_files"]
            input_err_txt = loc["CompressDialog.input_err"]
            files = FileDialog(input_files_txt, self).selectFiles(
                err_msg=input_err_txt)

            out_file_txt = loc["CompressDialog.output_file"]
            out_err_txt = loc["CompressDialog.output_err"]
            out_filter_txt = loc["CompressDialog.output_file_filter"]
            out_filter_txt = out_filter_txt.replace('|', ';')
            output_file = FileDialog(out_file_txt, self).selectSaveFile(
                err_msg=out_err_txt,
                filter=out_filter_txt)

            extra_args = self.config['Compression.extra_args'].split()
            extra_args.append(SevenZip.decode_file_format_arg(output_file))

            command = ["a"] + extra_args
            command += [output_file] + files
            self.sevenZip.start(command)
        except Exception as e:
            logger.error(f"{e}")
            QMessageBox.critical(self, f"Error", f"{e}")

    def on_click_btn_decompress(self):
        loc = self.localization
        try:
            input_files_txt = loc["DecompressDialog.input_file"]
            input_err_txt = loc["DecompressDialog.input_err"]
            input_filter_txt = loc["DecompressDialog.input_file_filter"]
            input_filter_txt = input_filter_txt.replace('|', ';')
            archive_file = FileDialog(
                input_files_txt, self
            ).selectFile(err_msg=input_err_txt, filter=input_filter_txt)

            out_dir_txt = loc["DecompressDialog.output_dir"]
            out_err_txt = loc["DecompressDialog.output_err"]
            output_dir = FileDialog(
                out_dir_txt, self
            ).selectDirectory(err_msg=out_err_txt)

            extra_args = self.config['Decompression.extra_args'].split()

            command = ["x", archive_file]
            command += [f"-o{output_dir}"]
            command += extra_args
            self.sevenZip.start(command)
        except Exception as e:
            logger.error(f"{e}")
            QMessageBox.critical(self, f"Error", f"{e}")

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
        msg_box_title = loc["OpFinish_MsgBox.title"]
        msg_box_succ = loc["OpFinish_MsgBox.content_succ"]
        msg_box_fail = loc["OpFinish_MsgBox.content_fail"]
        try:
            # Pattern (e.g., "Return code: 0")
            regex = Regex(r"Return code:.*(\d+)")
            match = regex.search(message)
            # Extract return code
            retcode = int(match.groups()[0])
            # Define user msg_box
            msg_box_func = QMessageBox.information if retcode == 0 else QMessageBox.critical
            msg_box_msg = msg_box_succ if retcode == 0 else msg_box_fail
            # show msg_box
            msg_box_func(self, msg_box_title, msg_box_msg)
        except Exception as e:
            pass
