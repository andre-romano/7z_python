import os
import logging

import tkinter as tk

from tkinter import messagebox

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class MsgBox:
    def __init__(self):
        pass

    def showInformation(self, title: str, text: str):
        logger.debug(f"(title={title} , text={text})")
        messagebox.showinfo(title, text)

    def showWarning(self, title: str, text: str):
        logger.debug(f"(title={title} , text={text})")
        messagebox.showwarning(title, text)

    def showCritical(self, title: str, text: str):
        logger.debug(f"(title={title} , text={text})")
        messagebox.showerror(title, text)

    def showQuestionYesNo(self, title: str, text: str, yes_callback=lambda: None, no_callback=lambda: None):
        """Displays YES/NO question"""
        callback = yes_callback if messagebox.askyesno(
            title, text, icon='question') else no_callback
        callback()
