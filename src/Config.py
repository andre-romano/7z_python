import logging
import os
import configparser

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        if not os.path.exists(config_file):
            self._create_sections()
            self.save_config()
        else:
            self.load_config()

    def _create_sections(self):
        self.set('Compression.extra_args', '-y -bb2 -mmt')

        self.set('Decompression.extra_args', '-y -bb2 -mmt')

        self.set('SFX.autorun', '')
        self.set('SFX.input_file', '')
        self.set('SFX.output_path', '')

    def load_config(self):
        """Carrega as configurações do arquivo INI """
        self.config.read(self.config_file, encoding='utf-8')

    def get(self, sec_option: str, fallback=None):
        """Obtém um valor da configuração com opção de fallback.
        Formato: 'secao.opcao' """
        section, option = sec_option.split('.')
        return self.config.get(section, option, fallback=fallback)

    def set(self, sec_option: str, value):
        """Define um valor na configuração.
        Formato: 'secao.opcao' """
        section, option = sec_option.split('.')
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))

    def save_config(self):
        """Salva as configurações no arquivo INI."""
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def show_all(self):
        """Mostra todas as configurações carregadas."""
        for section in self.config.sections():
            print(f"[{section}]")
            for key, value in self.config.items(section):
                print(f"{key} = {value}")
            print()
