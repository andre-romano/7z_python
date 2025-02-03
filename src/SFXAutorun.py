#!/bin/python3
import logging
import sys
import os

from PyQt6.QtWidgets import QWidget, QTextEdit

from widget.MsgBox import MsgBox

from process.SubprocessHandler import SubprocessHandler

# Create a logger for this module
logger = logging.getLogger(__name__)


class SFXAutorun:
    def __init__(self, env: dict, autorun: str, silent: str, parent: QWidget = None):
        self.env = env.copy()
        self.msgBox = MsgBox(parent)

        self.autorun = autorun.split()
        self.silent = False
        try:
            self.silent = (silent and int(silent) == 1)
        except Exception as e:
            logger.error(f"""Cannot convert 'silent' param '{
                         silent}' to bool. Error: {e}""")

        self.setLogOutput(None)
        self.setMsgBox('', '', '')

        self.subprocess = SubprocessHandler(
            env,
            start_callback=self.on_start,
            update_callback=self.on_update,
            finish_callback=self.on_finish
        )

    def setLogOutput(self, log_output: QTextEdit):
        self.log_output = log_output

    def setMsgBox(self, title: str, text_succ: str, text_fail: str):
        self.title = title
        self.text_succ = text_succ
        self.text_fail = text_fail

    def isSilent(self):
        return self.silent

    def start(self):
        self.run()

    def run(self):
        if not self.autorun:
            logger.info(f"No autorun detected.")
            self.on_finish()
            return

        self.subprocess.start(self.autorun)

    def on_start(self):
        pass

    def on_update(self, message: str):
        self.log_output.append(message)

    def on_finish(self):
        # show msgbox with the return code
        logger.debug(f"Return code: {self.subprocess.getReturnCode()}")
        if not self.isSilent():
            if self.subprocess.getReturnCode() == 0:
                self.msgBox.showInformation(self.title, self.text_succ)
            else:
                self.msgBox.showCritical(self.title, self.text_fail)
        sys.exit(0)
