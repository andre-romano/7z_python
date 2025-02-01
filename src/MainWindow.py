#!/bin/python3
import logging
import sys
import os

import tkinter as tk

from tkinter import ttk  # Importa o submódulo correto

from widget.FileDialog import FileDialog
from widget.MsgBox import MsgBox

from process.SevenZipHandler import SevenZipHandler
from process.SubprocessHandler import SubprocessHandler

from Config import Config
from Localization import Localization
from Regex import Regex

# Create a logger for this module
logger = logging.getLogger(__name__)


class MainWindow(tk.Frame):
    # operation modes
    MODE_NORMAL = 0
    MODE_SFX = 1

    def __init__(self, root: tk.Tk, data_path: str, debug=False):
        super().__init__(root)
        logger.info(f"(data_path={data_path}, debug={debug})")

        # set APP environment
        self.root = root
        self.mode = MainWindow.MODE_NORMAL
        self._setENV(data_path)

        # get config, localization, 7z_worker
        self.config = Config(self.env)
        self.localization = Localization(self.env)
        self.sevenZip = SevenZipHandler(
            self.env,
            self.on_7z_started,
            self.on_7z_update,
            self.on_7z_finish
        )
        self.sfxProcess = SubprocessHandler(
            self.env,
            self.on_sfx_start,
            self.on_sfx_update,
            self.on_sfx_finish
        )

        # create UI
        self._init_UI()

        # create auxiliary UI
        self.msgBox = MsgBox()  # Define msg box
        self.fileDialog = FileDialog()  # Define file dialog

        # check for SFX config
        # (after predefined delay -- allow UI to display)
        self.root.after(50, self.check_for_SFX)

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

    def _init_UI(self):
        loc = self.localization

        self.root.title("7-Zip Python Frontend")

        # Main Layout
        self.label = tk.Label(self.root, text=loc["Main.operation_label"])
        self.label.pack(pady=10)

        self.compress_button = tk.Button(
            self.root, text=loc["Main.compress_btn"], command=self.on_click_btn_compress)
        self.compress_button.pack(pady=5)

        self.decompress_button = tk.Button(
            self.root, text=loc["Main.decompress_btn"], command=self.on_click_btn_decompress)
        self.decompress_button.pack(pady=5)

        self.progress_bar = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(
            self.root, variable=self.progress_bar, maximum=100
        )
        self.progress.pack(pady=10, fill='x')

        self.log_output = tk.Text(self.root, height=10, wrap='word')
        self.log_output.pack(pady=5, fill='both', expand=True)

    def check_for_SFX(self):
        if not self.config['SFX.input_file']:
            return

        # get localization
        loc = self.localization
        title = loc['SFX_MsgBox.title']
        text = loc['SFX_MsgBox.content']

        if self.config['SFX.silent'] == "1":
            self.on_sfx_decompress()
        else:
            # question user
            self.msgBox.showQuestionYesNo(
                title,
                text,
                yes_callback=self.on_sfx_decompress
            )

    def on_sfx_decompress(self):
        self.mode = MainWindow.MODE_SFX

        input_file = self.config['SFX.input_file']
        output_dir = self.config['SFX.output_path']
        extra_args = self.config['Decompression.extra_args']
        self.sevenZip.startDecompress(input_file, output_dir, extra_args)

    def on_click_btn_compress(self):
        loc = self.localization
        try:
            title = loc["CompressDialog.input_files"]
            err_msg = loc["CompressDialog.input_err"]
            input_files = self.fileDialog.selectFiles(
                title, err_msg)

            title = loc["CompressDialog.output_file"]
            err_msg = loc["CompressDialog.output_err"]
            filter = loc["CompressDialog.output_file_filter"]
            output_file = self.fileDialog.selectSaveFile(
                title, err_msg, filter=filter)

            self.sevenZip.startCompress(
                input_files, output_file, self.config['Compression.extra_args'])
        except Exception as e:
            logger.error(f"{e}")
            self.msgBox.showCritical(f"Error", f"{e}")

    def on_click_btn_decompress(self):
        loc = self.localization
        try:
            title = loc["DecompressDialog.input_file"]
            err_msg = loc["DecompressDialog.input_err"]
            filter = loc["DecompressDialog.input_file_filter"]
            input_file = self.fileDialog.selectFile(
                title, err_msg, filter=filter)

            title = loc["DecompressDialog.output_dir"]
            err_msg = loc["DecompressDialog.output_err"]
            output_dir = self.fileDialog.selectDirectory(
                title, err_msg)

            self.sevenZip.startDecompress(
                input_file, output_dir, self.config['Decompression.extra_args'])
        except Exception as e:
            logger.error(f"{e}")
            self.msgBox.showCritical(f"Error", f"{e}")

    def on_7z_started(self):
        self.log_output.delete(1.0, tk.END)
        self.progress_bar.set(0)

    def on_7z_update(self, message: str):
        # logger.debug(message)
        self.log_output.insert(tk.END, message + '\n')
        self.update_7z_progress(message)

    def on_7z_finish(self):
        self.log_output.insert(tk.END, "\n")
        self.progress_bar.set(100)

        # is in SFX mode
        if self.mode == MainWindow.MODE_SFX and self.config['SFX.autorun']:
            autorun_cmd = self.config['SFX.autorun'].split()
            self.sfxProcess.start(autorun_cmd)
        else:
            self.showOpFinishedMsgBox(self.sevenZip)

    def on_sfx_start(self):
        self.log_output.insert(tk.END, "\n")

    def on_sfx_update(self, message: str):
        self.log_output.insert(tk.END, message + '\n')

    def on_sfx_finish(self):
        # show msgbox with the return code
        if not (self.config['SFX.silent'] == "1"):
            self.showOpFinishedMsgBox(self.sfxProcess)
        # quit app
        self.root.quit()

    def update_7z_progress(self, message):
        try:
            # Search for progress percentage in the message using the regex pattern
            # (e.g., "Extracting: 23%")
            regex = Regex(r"(Compressing|Extracting).*\s(\d+)%")
            match = regex.search(message)
            # Extract percentage
            operation, percentage = match.groups()
            percentage = int(percentage)
            # Update the progress bar value
            self.progress_bar.set(percentage)
        except Exception as e:
            pass

    def showOpFinishedMsgBox(self, subprocess: SubprocessHandler):
        # get localization
        loc = self.localization
        title = loc["OpFinish_MsgBox.title"]
        text_succ = loc["OpFinish_MsgBox.content_succ"]
        text_fail = loc["OpFinish_MsgBox.content_fail"]

        # show msgbox with the return code
        if subprocess.getReturnCode() == 0:
            self.msgBox.showInformation(title, text_succ)
        else:
            self.msgBox.showCritical(title, text_fail)
