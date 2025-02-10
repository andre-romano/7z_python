import logging
import os
import configparser

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class ConfigParser:
    def __init__(self, filename: str, create_default: bool = False):
        self.config = configparser.ConfigParser()
        self.setFilename(filename)

        try:
            if filename:
                self.load()
        except:
            if filename and create_default:
                self._init_default_data()
                self.save()

    def __getitem__(self, sec_option: str):
        return self.get(sec_option)

    def __setitem__(self, sec_option: str, value):
        return self.set(sec_option, value)

    def _init_default_data(self):
        logger.warning(f"NOT overloaded")

    def get(self, sec_option: str, fallback=''):
        """Obtém um valor da configuração com opção de fallback.
        Formato: 'secao.opcao' """
        section, option = sec_option.split('.')
        return str(self.config.get(section, option, fallback=fallback)).strip()

    def set(self, sec_option: str, value):
        """Define um valor na configuração.
        Formato: 'secao.opcao' """
        section, option = sec_option.split('.')
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))

    def show_all(self):
        """Mostra todas as configurações carregadas."""
        for section in self.config.sections():
            print(f"[{section}]")
            for key, value in self.config.items(section):
                print(f"{key} = {value}")
            print()

    def setFilename(self, filename: str):
        self.filename = filename

    def load(self):
        """Carrega as configurações do arquivo INI """
        if (not self.filename) or (not os.path.exists(self.filename)):
            msg = f"File '{self.filename}' not found"
            logger.error(msg)
            raise FileNotFoundError(msg)
        logger.info(f"Reading file '{self.filename}' ...")
        self.config.read(self.filename, encoding='utf-8')

    def save(self):
        """Salva as configurações no arquivo INI."""
        logger.info(f"Saving file '{self.filename}' ...")
        with open(self.filename, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
