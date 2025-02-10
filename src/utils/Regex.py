

import logging
import re

# Create a logger for this module
logger = logging.getLogger(__name__)


class Regex:
    def __init__(self, *args):
        if len(args) < 1:
            raise Exception("No pattern or compiled regex provided")

        if isinstance(args[0], str):
            self.regex = re.compile(args[0])
        elif isinstance(args[0], re.Pattern):
            self.regex = args[0]
        else:
            raise Exception(f"Unable to create instance with args '{args}'")

    def search(self, message: str):
        match = self.regex.search(message)
        if not match:
            raise Exception(
                f"Regex '{self.regex}' not found in message '{message}'")
        return match

    @staticmethod
    def compile(pattern: str):
        return Regex(pattern)
