import logging
import os

from utils.ConfigParser import ConfigParser
from utils.SingletonAbstract import SingletonAbstract

from Environment import Environment

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class Config(ConfigParser, SingletonAbstract):
    def __init__(self):
        env = Environment.getInstance()

        super().__init__(env['CONFIG_FILE'], create_default=True)

    def _init_default_data(self):
        self.set('Compression.extra_args', '-y -bb2 -mmt')

        self.set('Decompression.extra_args', '-y -bb2 -mmt')

        self.set('SFX.autorun', '')
        self.set('SFX.input_file', '')
        self.set('SFX.output_path', '')
        self.set('SFX.silent', '')
