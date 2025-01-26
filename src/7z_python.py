#!/bin/python3

import sys
import os
import logging

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow
from Regex import Regex

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

lib_path = data_path + f"{os.path.sep}lib"

# register paths in sys.path (PATH env)
paths = [script_path, data_path, lib_path]
for path in paths:
    sys.path.insert(0, path)
    os.environ['PATH'] += f"{path};"

# Change the current working directory to the script's directory
os.chdir(script_path)

if __name__ == "__main__":
    # TODO set debug to FALSE
    debug = True

    # setup logging
    if os.path.exists(logfile):
        os.remove(logfile)
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - [%(levelname)s]\t-  %(name)s.%(funcName)s():  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(logfile),  # Log to file
            logging.StreamHandler()                  # Log to console
        ]
    )

    # start app
    app = QApplication(sys.argv)
    mainWindow = MainWindow(
        data_path,
        debug=debug
    )
    mainWindow.show()
    sys.exit(app.exec_())
