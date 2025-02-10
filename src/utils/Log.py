import logging
import os

from logging import FileHandler

from PySide6.QtCore import QTimer


class Log:

    @staticmethod
    def config(logfile: str | None = None, debug: bool = True):
        """Configures the logging system."""
        log_level = logging.DEBUG if debug else logging.INFO

        # Remove old log file (optional rotation strategy)
        if logfile and os.path.exists(logfile):
            os.remove(logfile)

        # Set up log handlers
        handlers: list[logging.Handler] = [
            logging.StreamHandler()  # Console logging
        ]
        if logfile:
            handlers.append(FileHandler(logfile))

        # Configure logging
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - [%(levelname)s] - %(name)s.%(funcName)s(): %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=handlers,
        )

    @staticmethod
    def _flushLogs():
        """Flushes all log handlers to ensure logs are written to disk."""
        logger = logging.getLogger(__name__)  # Class-level logger

        for logger_name in logging.root.manager.loggerDict:
            _logger = logging.getLogger(logger_name)
            for handler in _logger.handlers:
                handler.flush()
        logger.debug("Flushed all logs")

    @staticmethod
    def scheduleFlushLogs(interval_ms: int):
        """Schedules periodic log flushing using QTimer."""
        timer = QTimer()
        # Fixed: Removed incorrect () call
        timer.timeout.connect(Log._flushLogs)
        timer.start(interval_ms)  # Run every `interval_ms` milliseconds
