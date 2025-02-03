import logging
import sys
import os

# Create a logger for this module
logger = logging.getLogger(__name__)


class Callbacks:
    def __init__(self, *callbacks):
        self.callbacks = []
        for callback in callbacks:
            if not callable(callback):
                continue
            self.append(callback)

    def append(self, callback):
        self.callbacks.append(callback)

    def run(self, *args):
        for callback in self.callbacks:
            callback(*args)
