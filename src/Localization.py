import logging
import os
import configparser

# Create a logger for this module
logger = logging.getLogger(__name__)


class Localization:
    def __init__(self, locale_dir, lang=None, default_lang="en"):
        """
        Initialize the localization system.

        :param locale_dir: Directory where the .ini localization files are stored.
        :param default_lang: Default language to load.
        """
        self.locale_dir = locale_dir
        self.current_lang = default_lang
        self.translations = {}
        try:
            self.load_language(lang)
        except Exception as e:
            logger.error(f"Fail to load language '{lang}'. Error: {e}")
            try:
                self.load_language(default_lang)
            except Exception as e:
                logger.error(f"Fail to load language '{
                             default_lang}'. Error: {e}")

    def load_language(self, lang_code):
        """
        Load translations from an INI file based on the given language code.

        :param lang_code: Language code (e.g., 'en', 'es', 'fr').
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

        self.current_lang = lang_code

    def translate(self, key, default=None) -> str:
        """
        Retrieve a translated string for the given key.

        :param key: The key to look up (e.g., 'general.greeting').
        :param default: Default value to return if key is not found.
        :return: Translated string or the default value.
        """
        return self.translations.get(key, default or f"[{key}]")

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
