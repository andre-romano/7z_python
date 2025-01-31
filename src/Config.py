import logging
import os
import configparser

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class Config:
    def __init__(self, env: dict):
        self.env = env
        self.config_file = env['CONFIG_FILE']
        self.config = configparser.ConfigParser()

        if not os.path.exists(self.config_file):
            self._init_default_data()
            self.save_config()
        else:
            self.load_config()

    def __getitem__(self, sec_option: str):
        return self.get(sec_option)

    def __setitem__(self, sec_option: str, value):
        return self.set(sec_option, value)

    def _init_default_data(self):
        self.set('Compression.extra_args', '-y -bb2 -mmt')

        self.set('Decompression.extra_args', '-y -bb2 -mmt')

        self.set('SFX.autorun', '')
        self.set('SFX.input_file', '')
        self.set('SFX.output_path', '')
        self.set('SFX.silent', '')

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

    def load_config(self):
        """Carrega as configurações do arquivo INI """
        self.config.read(self.config_file, encoding='utf-8')

    def save_config(self):
        """Salva as configurações no arquivo INI."""
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
