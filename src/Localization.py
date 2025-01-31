import logging
import os
import configparser

# Create a logger for this module
logger = logging.getLogger(__name__)


class Localization:
    def __init__(self, env: dict):
        """
        Initialize the localization system.
        """
        self.env = env
        self.locale_dir = self.env['LOCALE_PATH']
        self.translations = {}

        try:
            self.load_language(self.env['LANG'])
        except Exception as e:
            logger.error(
                f"Fail to load language '{self.env['LANG']}'. Error: {e}")
            self.load_language(self.env['LANG_DEFAULT'])

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=None) -> str:
        """
        Retrieve a translated string for the given key.

        :param key: The key to look up (e.g., 'general.greeting').
        :param default: Default value to return if key is not found.
        :return: Translated string or the default value.
        """
        return self.translations.get(key, default or f"[{key}]")

    def load_language(self, lang_code: str):
        """
        Load translations from an INI file based on the given language code.

        :param lang_code: Language code (e.g., 'en', 'es', 'fr').
        :raise Exception if language not found
        """
        ini_file = os.path.join(self.locale_dir, f"{lang_code}.ini")

        if not os.path.exists(ini_file):
            raise FileNotFoundError(f"Localization file '{
                                    ini_file}' not found")

        config = configparser.ConfigParser()
        config.read(ini_file, encoding='utf-8')

        self.translations.clear()
        for section in config.sections():
            for key, value in config.items(section):
                self.translations[f"{section}.{key}"] = value

    def set_language(self, lang_code):
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
