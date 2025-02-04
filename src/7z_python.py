#!/bin/python3

import sys
import os
import logging

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
from Regex import Regex


def load_file(filename):
    with open(filename, "r") as file:
        return file.read()


# get filename
filename = os.path.basename(__file__).split(".")[0]
logfile = f'{filename}.log'

# Get the absolute path to the script directory
script_path = os.path.abspath(os.path.dirname(__file__))
data_path = f"{script_path}{os.path.sep}data"

try:
    # Get data directory
    regex = Regex(r"^(.*)[\\/]src")
    data_path = regex.search(script_path).groups()[0]+f"{os.path.sep}data"
except:
    pass

# get UI path
ui_path = f"{data_path}{os.path.sep}ui"

# place script path in PATH env
sys.path.insert(0, script_path)

# Change the current working directory to the script's directory
# os.chdir(script_path)

if __name__ == "__main__":
    # TODO set debug to FALSE
    debug = True

    # remove old log file (log file rotation here ?)
    if os.path.exists(logfile):
        os.remove(logfile)

    # setup logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - [%(levelname)s]\t-  %(name)s.%(funcName)s():  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(logfile),  # Log to file
            logging.StreamHandler()                  # Log to console
        ]
    )

    # Create a logger for this module
    logger = logging.getLogger(__name__)

    # start app (safely catch errors and log'em)
    try:
        app = QApplication(sys.argv)

        # load QSS styles
        qss = load_file(f"{ui_path}{os.path.sep}styles.qss")
        app.setStyleSheet(qss)

        # display main window
        mainWindow = MainWindow(
            data_path,
            debug=debug
        )
        mainWindow.show()

        # terminate app
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Uncaught Error: {e}")
        sys.exit(1)
