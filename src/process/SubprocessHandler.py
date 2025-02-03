import logging
import sys
import os

from multiprocessing import Queue

from PyQt6.QtCore import pyqtSignal, QObject

from Callbacks import Callbacks

from process.SubprocessWorker import SubprocessWorker

# Create a logger for this module
logger = logging.getLogger(__name__)


class SubprocessHandler(QObject):
    progress = pyqtSignal(int)

    def __init__(self, env, start_callback=None, update_callback=None, finish_callback=None):
        super().__init__()

        self.env = env
        self._setENV()

        self.start_callbacks = Callbacks(start_callback)
        self.update_callbacks = Callbacks(update_callback)
        self.finish_callbacks = Callbacks(finish_callback)

        # monitor subprocess progress
        self.progress.emit(0)

        self.command = []
        self._setReturnCode(0)

    def _setENV(self):
        logger.warning("Not overriden")

    def run(self):
        logger.info(f"(command={self.command})")
        self._setReturnCode(-1)

        if not self.command:
            raise Exception(f"Command is empty")

        # process start callback
        self.start_callbacks.run()
        self.progress.emit(0)

        # create queue
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
        self._setReturnCode(worker.getReturnCode())

        # process finished
        self.finish_callbacks.run()
        self.progress.emit(100)

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
