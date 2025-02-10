import logging
import os

from utils.SingletonAbstract import SingletonAbstract
from utils.SafeDict import SafeDict

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class Environment(SafeDict, SingletonAbstract):
    def __init__(self, dictObj: dict | None = None):
        super().__init__(dictObj)
        logger.info(f"Creating Environment ...")
        self._setLang()

    def _setLang(self):
        # language config
        self['LANG_DEFAULT'] = 'en'
        self['LANG'] = self.get('LANG', self['LANG_DEFAULT'])
        self['LANG'] = self['LANG'].split('_')[0].split('-')[0]
        logger.info(f"LANG = {self['LANG']}")

    def _setFiles(self):
        self['LOG_FILE'] = f"7z_python.log"
        self['CONFIG_FILE'] = f"7z_python.ini"
        self['QSS_FILE'] = f"{self['UI_PATH']}{os.path.sep}styles.qss"

        logger.debug(f"QSS = {self['QSS_FILE']}")
        logger.debug(f"LOG = {self['LOG_FILE']}")
        logger.debug(f"CFG = {self['CONFIG_FILE']}")

    def _setSevenZip(self):
        self['7ZIP_BIN'] = f"{self['DATA_PATH']}{os.path.sep}lib"
        self['7ZIP'] = f"{self['7ZIP_BIN']}{os.path.sep}7z.exe"

        logger.debug(f"7Z_BIN = {self['7ZIP_BIN']}")
        logger.debug(f"7Z_EXE = {self['7ZIP']}")

    def setPaths(self, data_path: str):
        self["DATA_PATH"] = data_path
        self['UI_PATH'] = f"{data_path}{os.path.sep}ui"
        self['LOCALE_PATH'] = f"{data_path}{os.path.sep}lang"

        logger.debug(f"  DATA_PATH = {self['DATA_PATH']}")
        logger.debug(f"    UI_PATH = {self['UI_PATH']}")
        logger.debug(f"LOCALE_PATH = {self['LOCALE_PATH']}")

        self._setFiles()
        self._setSevenZip()

    def setDebug(self, debug: bool):
        self["DEBUG_MODE"] = str(debug)
        logger.debug(f"DEBUG_MODE = {self['DEBUG_MODE']}")
