import os
import logging

from PyQt6.QtWidgets import QWidget, QMessageBox

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class MsgBox:
    StandardButton = QMessageBox.StandardButton  # Alias for shorter references

    def __init__(self, parent: QWidget = None):
        self.parent = parent

    def showInformation(self, title: str, text: str):
        logger.debug(f"(title={title} , text={text})")
        return QMessageBox.information(self.parent, title, text)

    def showWarning(self, title: str, text: str):
        logger.debug(f"(title={title} , text={text})")
        return QMessageBox.warning(self.parent, title, text)

    def showCritical(self, title: str, text: str):
        logger.debug(f"(title={title} , text={text})")
        return QMessageBox.critical(self.parent, title, text)

    def showQuestion(self, title: str, text: str, default_btn: StandardButton, btn_callback_list: list):
        """Displays a question using btns, with a default btn
        :param btn_callback_list list of btn and respective callback in the format [(btn, callback(btn)), ...] """
        if not btn_callback_list:
            raise Exception("Empty btn_callback_list")

        # build btn list based on callbacks provided
        btns = btn_callback_list[0][0]
        for btn, _ in btn_callback_list:
            btns = btns | btn

        logger.debug(f"""(title={title} , text={text}, btns={
                     btns}, default_btn={default_btn}, btn_callback_list={btn_callback_list})""")
        res = QMessageBox.question(self.parent, title, text, btns, default_btn)
        for btn, callback in btn_callback_list:
            if res == btn:
                logger.debug(f"Answer {res}")
                callback()
                break

    def showQuestionYesNo(self, title: str, text: str, default_btn: StandardButton = StandardButton.No, yes_callback=lambda: None, no_callback=lambda: None):
        """Displays YES/NO question"""
        self.showQuestion(title, text, default_btn, btn_callback_list=[
            (self.StandardButton.Yes, yes_callback),
            (self.StandardButton.No, no_callback),
        ])

    def showQuestionSaveDiscard(self, title: str, text: str, default_btn: StandardButton = StandardButton.Discard, save_callback=lambda: None, discard_callback=lambda: None):
        """Displays SAVE/DISCARD question"""
        self.showQuestion(title, text, default_btn, btn_callback_list=[
            (self.StandardButton.Save, save_callback),
            (self.StandardButton.Discard, discard_callback),
        ])
