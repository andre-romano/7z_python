
import logging

from threading import RLock

# Set up logger (you may have already set this up elsewhere in your application)
logger = logging.getLogger(__name__)


class SafeDict:
    def __init__(self, dictObj: dict | None = None):
        """Initialize a shared dictionary with a Lock for thread safety."""
        self._dict = dictObj or {}
        self._lock = RLock()

    def set(self, key, value):
        """Safely set a key-value pair in the dictionary."""
        with self._lock:
            self._dict[key] = value

    def get(self, key, default=None):
        """Safely retrieve a value from the dictionary."""
        with self._lock:
            return self._dict.get(key, default)

    def delete(self, key):
        """Safely delete a key from the dictionary."""
        with self._lock:
            if key in self._dict:
                del self._dict[key]

    def keys(self):
        """Return a list of dictionary keys."""
        with self._lock:
            return list(self._dict.keys())

    def values(self):
        """Return a list of dictionary values."""
        with self._lock:
            return list(self._dict.values())

    def items(self):
        """Return a list of dictionary items (key-value pairs)."""
        with self._lock:
            return list(self._dict.items())

    def clear(self):
        """Safely clear the dictionary."""
        with self._lock:
            self._dict.clear()

    def copy(self):
        """Safely copy the dictionary."""
        with self._lock:
            return SafeDict(self._dict.copy())

    def copyDict(self):
        """Copy internal dictionary (return dict)."""
        with self._lock:
            return self._dict.copy()

    def __getitem__(self, key):
        """Safely retrieve a value from the dictionary using bracket notation."""
        with self._lock:
            if key not in self._dict:
                msg = f"Key '{key}' not found."
                logger.error(msg)
                raise KeyError(msg)
            return self._dict[key]

    def __setitem__(self, key, value):
        """Safely retrieve a value from the dictionary using bracket notation."""
        with self._lock:
            self._dict[key] = value

    def __delitem__(self, key):
        with self._lock:
            del self._dict[key]

    def __contains__(self, key):
        with self._lock:
            return key in self._dict

    def __len__(self):
        with self._lock:
            return len(self._dict)

    def __repr__(self):
        """Return a string representation of the dictionary."""
        with self._lock:
            return repr(self._dict)
