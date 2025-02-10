import logging
import os

from Environment import Environment

from utils.SingletonAbstract import SingletonAbstract

from utils.ConfigParser import ConfigParser

# Create a logger for this module
logger = logging.getLogger(__name__)


class Localization(ConfigParser, SingletonAbstract):
    def __init__(self):
        """
        Initialize the localization system.
        """
        super().__init__('')

        env = Environment.getInstance()
        self.locale_dir = env['LOCALE_PATH']
        logger.debug(f"locale_dir = {self.locale_dir}")

        try:
            self.load_language(env['LANG'])
        except Exception as e:
            logger.error(
                f"Fail to load language '{env['LANG']}'. Error: {e}")
            self.load_language(env['LANG_DEFAULT'])

    def load_language(self, lang_code: str):
        """
        Load translations from an INI file based on the given language code.

        :param lang_code: Language code (e.g., 'en', 'es', 'fr').
        :raise Exception if language not found
        """
        logger.info(f"Loading language '{lang_code}' ...")
        ini_file = os.path.join(self.locale_dir, f"{lang_code}.ini")
        self.setFilename(ini_file)

        self.load()

    def set_language(self, lang_code: str):
        """
        Change the current language.

        :param lang_code: Language code (e.g., 'en', 'fr').
        """
        self.load_language(lang_code)

    def available_languages(self):
        """
        Get a list of available languages based on the existing INI files.

        :return: List of language codes.
        """
        files = os.listdir(self.locale_dir)
        available = [f.split('.')[0] for f in files if f.endswith('.ini')]
        logger.info(f"Languages = {available}")
        return available
