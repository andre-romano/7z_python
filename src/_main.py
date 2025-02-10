#!/bin/python3

import logging
import re
import sys
import os

from PySide6.QtWidgets import QApplication

from utils.Log import Log

from Environment import Environment
from MainWindow import MainWindow


def load_file(filename):
    with open(filename, "r") as file:
        return file.read()


# get filename
filename = os.path.basename(__file__).split(".")[0]

# Get the absolute path to the script directory
script_path = os.path.abspath(os.path.dirname(__file__))
data_path = f"{script_path}{os.path.sep}data"

# Get data directory
regex = re.compile(r"^(.*)[\\/]src")
match = regex.search(script_path)
if match:
    data_path = match.groups()[0]+f"{os.path.sep}data"

# place script path in PATH env
sys.path.insert(0, script_path)

# Change the current working directory to the script's directory
# os.chdir(script_path)

if __name__ == "__main__":
    # Configure environment
    env = Environment.getInstance(os.environ.copy())
    env.setDebug(True)
    env.setPaths(data_path)

    # config logger (terminal + logfile)
    Log.config(
        logfile=env['LOG_FILE'],
        debug=env['DEBUG_MODE'] == "True"
    )
    logger = logging.getLogger(__name__)

    # start app (safely catch errors and log'em)
    try:
        # start app
        logger.info(f"Starting app ...")
        app = QApplication(sys.argv)

        # load QSS styles
        logger.debug(f"Loading QSS file '{env['QSS_FILE']}' ...")
        qss = load_file(env['QSS_FILE'])
        app.setStyleSheet(qss)

        # display main window
        logger.debug(f"Opening main window ...")
        mainWindow = MainWindow()
        mainWindow.show()

        # terminate app
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Uncaught Error: {e}")
        sys.exit(1)
