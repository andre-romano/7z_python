import logging
import os
import configparser

from Environment import Environment

from utils.SingletonAbstract import SingletonAbstract
from utils.SafeDict import SafeDict

# Create a logger for this module
logger = logging.getLogger(__name__)


class Localization(SafeDict, SingletonAbstract):
    def __init__(self):
        """
        Initialize the localization system.
        """
        super().__init__()

        env = Environment.getInstance()
        self.locale_dir = env['LOCALE_PATH']
        logger.debug(f"locale_dir = {self.locale_dir}")

        try:
            self.load_language(env['LANG'])
        except Exception as e:
            logger.error(
                f"Fail to load language '{env['LANG']}'. Error: {e}")
            self.load_language(env['LANG_DEFAULT'])

    def __getitem__(self, key: str):
        return self.get(key)

    def get(self, key: str, default: str | None = None):
        """
        Retrieve a translated string for the given key.

        :param key: The key to look up (e.g., 'general.greeting').
        :param default: Default value to return if key is not found.
        :return: Translated string or the default value.
        """
        return str(super().get(key, default or f"[{key}]")).strip()

    def load_language(self, lang_code: str):
        """
        Load translations from an INI file based on the given language code.

        :param lang_code: Language code (e.g., 'en', 'es', 'fr').
        :raise Exception if language not found
        """
        logger.info(f"Loading language '{lang_code}' ...")
        ini_file = os.path.join(self.locale_dir, f"{lang_code}.ini")

        if not os.path.exists(ini_file):
            msg = f"Localization file '{ini_file}' not found"
            logger.error(msg)
            raise FileNotFoundError(msg)

        logger.info(f"Reading INI file '{ini_file}' ...")
        configParser = configparser.ConfigParser()
        configParser.read(ini_file, encoding='utf-8')

        self.clear()
        for section in configParser.sections():
            for key, value in configParser.items(section):
                new_key = f"{section}.{key}"
                self[new_key] = value
                # logger.debug(f"self[{section}.{key}] = {self[new_key]}")

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
        return [f.split('.')[0] for f in files if f.endswith('.ini')]
