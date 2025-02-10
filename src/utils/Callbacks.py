
import logging

from typing import Callable, Iterable

from datatype.SafeList import SafeList

# Create a logger for this module
logger = logging.getLogger(__name__)


class Callbacks:
    def __init__(self, *callbacks):
        self.callbacks = SafeList()
        self.extend(callbacks)

    def extend(self, callbacks: Iterable[Callable]):
        for callback in callbacks:
            self.append(callback)

    def append(self, callback: Callable):
        if not callable(callback):
            return
        self.callbacks.append(callback)

    def run(self, *args):
        for callback in self.callbacks:
            callback(*args)

    def connect(self, callback: Callable):
        self.append(callback)

    def emit(self, *args):
        self.run(*args)
