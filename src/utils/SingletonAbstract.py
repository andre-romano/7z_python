import logging

from threading import RLock
from typing import Self

from datatype.SafeDict import SafeDict

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class SingletonAbstract:
    _instances = SafeDict()
    _instances_lock = RLock()

    @classmethod
    def getInstance(cls, *args, **kwargs) -> Self:
        # Check if class instance exists
        with cls._instances_lock:
            if cls.__name__ not in cls._instances:
                logger.info(f"Creating instance for '{cls.__name__}' ...")
                cls._instances[cls.__name__] = cls(*args, **kwargs)
        return cls._instances[cls.__name__]
