#!/bin/python3
import logging

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer, QObject

from ui.MainWindow import Ui_MainWindow  # Import the generated UI class

from utils.Regex import Regex
from utils.Log import Log

from widget.FileDialog import FileDialog
from widget.MsgBox import MsgBox

from SevenZipHandler import SevenZipHandler
from Config import Config
from Localization import Localization
from Environment import Environment
from SFXAutorun import SFXAutorun

# Create a logger for this module
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow, QObject):
    def __init__(self):
        super().__init__()
        logger.info(f" ")

        # set APP environment
        env = Environment.getInstance()
        env["APP_MODE"] = "NORMAL"

        # get config, localization, 7z_worker
        self.config = Config()
        self.sevenZip = SevenZipHandler(
            self.on_7z_started,
            self.on_7z_update,
            self.on_7z_finish,
            env=env.copyDict()
        )
        self.sevenZip.addProgressCallback(
            lambda progress: self.progress_bar.setValue(progress))

        # create and configure UI
        self._init_UI()

        # create auxiliary UI
        self.msgBox = MsgBox(self)  # Define msg box
        self.fileDialog = FileDialog(self)  # Define file dialog
        self.sfxAutorun = SFXAutorun(
            parent=self,
            env=Environment.getInstance().copyDict(),
            autorun=self.config['SFX.autorun'],
            silent=self.config['SFX.silent']
        )

        # schedule log flushing
        Log.scheduleFlushLogs(5000)

        # check for SFX config
        # (after predefined delay -- allow UI to display)
        QTimer.singleShot(50, self.check_for_SFX)

    def _init_UI(self):
        self.setupUi(self)  # create GUI

        loc = Localization.getInstance()  # translate the GUI

        label_txt = loc["Main.operation_label"]
        self.label.setText(label_txt)

        compress_btn_txt = loc["Main.compress_btn"]
        self.compress_button.setText(compress_btn_txt)
        self.compress_button.clicked.connect(self.on_click_btn_compress)

        decompress_btn_txt = loc["Main.decompress_btn"]
        self.decompress_button.setText(decompress_btn_txt)
        self.decompress_button.clicked.connect(self.on_click_btn_decompress)

    def check_for_SFX(self):
        if not self.config['SFX.input_file']:
            return

        # get localization
        loc = Localization.getInstance()
        title = loc['SFX_MsgBox.title']
        text = loc['SFX_MsgBox.content']

        if self.sfxAutorun.isSilent():
            self.on_sfx_decompress()
        else:
            # question user
            self.msgBox.showQuestionYesNo(
                title,
                text,
                default_btn=MsgBox.StandardButton.Yes,
                yes_callback=self.on_sfx_decompress
            )

    def on_sfx_decompress(self):
        env = Environment.getInstance()
        env['APP_MODE'] = 'SFX'

        input_file = self.config['SFX.input_file']
        output_dir = self.config['SFX.output_path']
        extra_args = self.config['Decompression.extra_args']
        self.sevenZip.startDecompress(input_file, output_dir, extra_args)

    def on_click_btn_compress(self):
        loc = Localization.getInstance()
        try:
            title = loc["CompressDialog.input_files"]
            err_msg = loc["CompressDialog.input_err"]
            input_files = self.fileDialog.selectFiles(
                title, err_msg)

            title = loc["CompressDialog.output_file"]
            err_msg = loc["CompressDialog.output_err"]
            filter = loc["CompressDialog.output_file_filter"]
            filter = filter.replace('|', ';')
            output_file = self.fileDialog.selectSaveFile(
                title, err_msg, filter=filter)

            self.sevenZip.startCompress(
                input_files, output_file, self.config['Compression.extra_args'])
        except Exception as e:
            logger.error(f"{e}")
            self.msgBox.showCritical(f"Error", f"{e}")

    def on_click_btn_decompress(self):
        loc = Localization.getInstance()
        try:
            title = loc["DecompressDialog.input_file"]
            err_msg = loc["DecompressDialog.input_err"]
            filter = loc["DecompressDialog.input_file_filter"]
            filter = filter.replace('|', ';')
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
        self.log_output.clear()

    def on_7z_update(self, message: str):
        logger.debug(message)
        self.log_output.append(message)

    def on_7z_finish(self):
        self.log_output.append(" ")

        # get localization
        loc = Localization.getInstance()
        title = loc["OpFinish_MsgBox.title"]
        text_succ = loc["OpFinish_MsgBox.content_succ"]
        text_fail = loc["OpFinish_MsgBox.content_fail"]

        # is in SFX mode
        env = Environment.getInstance()
        if env['APP_MODE'] == 'SFX':
            # define SFX autorun GUI
            self.sfxAutorun.setLogOutput(self.log_output)
            self.sfxAutorun.setMsgBox(title, text_succ, text_fail)

            # start SFX autorun
            self.sfxAutorun.start()
        else:
            # show msgbox with the return code
            if self.sevenZip.getReturnCode() == 0:
                self.msgBox.showInformation(title, text_succ)
            else:
                self.msgBox.showCritical(title, text_fail)
