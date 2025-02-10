import logging

from multiprocessing import Queue

from PySide6.QtCore import Signal, QObject

from utils.Callbacks import Callbacks
from utils.SubprocessWorker import SubprocessWorker

# Create a logger for this module
logger = logging.getLogger(__name__)


class SubprocessHandler(QObject):
    progress = Signal(int)

    def __init__(self, start_callback=None, update_callback=None, finish_callback=None, env: dict | None = None):
        super().__init__()

        self.env = env or {}

        self.start_callbacks = Callbacks(start_callback)
        self.update_callbacks = Callbacks(update_callback)
        self.finish_callbacks = Callbacks(finish_callback)

        # monitor subprocess progress
        self.progress.emit(0)

        self.command = []
        self._setReturnCode(0)

    def run(self):
        logger.info(f"(command={self.command})")
        self._setReturnCode(-1)

        if not self.command:
            raise Exception(f"Command is empty")

        # process start callback
        self.start_callbacks.run()
        self.progress.emit(0)

        # create queue and environment
        queue = Queue()

        # Start the worker process
        logger.info("Starting worker ...")
        worker = SubprocessWorker(self.command, queue, env=self.env)
        worker.start()

        # Process the output from the worker process
        self._handle_output(queue, worker)

    def _handle_output(self, queue: Queue, worker: SubprocessWorker):
        # Process the queue's output in the main thread
        while worker.isRunning():
            while not queue.empty():
                message = queue.get()
                logger.info(message)
                self.update_callbacks.run(message)

        logger.info(" ")
        logger.info("Waiting for Worker ...")
        worker.wait()
        logger.info("Worker TERMINATED")

        # process finished
        self._setReturnCode(worker.getReturnCode())
        self.finish_callbacks.run()
        self.progress.emit(100)

        # To flush the logger and any handlers
        for handler in logger.handlers:
            handler.flush()

    def addStartCallback(self, callback):
        self.start_callbacks.append(callback)

    def addUpdateCallback(self, callback):
        self.update_callbacks.append(callback)

    def addFinishCallback(self, callback):
        self.finish_callbacks.append(callback)

    def connectProgress(self, callback):
        return self.progress.connect(callback)

    def _setReturnCode(self, returncode: int):
        self.returncode = returncode

    def getReturnCode(self):
        return self.returncode

    def start(self, command: list):
        self.command = command
        self.run()
