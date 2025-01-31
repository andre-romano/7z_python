import logging
import sys
import os
import shutil

from multiprocessing import Queue

from Regex import Regex

from process.SubprocessWorker import SubprocessWorker

# Create a logger for this module
logger = logging.getLogger(__name__)


class SubprocessHandler:
    def __init__(self, env, start_callback=None, update_callback=None, finish_callback=None):
        super().__init__()

        self.env = env
        self._setENV()

        self.start_callback = start_callback or (lambda: None)
        self.update_callback = update_callback or (lambda: None)
        self.finish_callback = finish_callback or (lambda: None)

        self.command = []
        self._setReturnCode(0)

    def _setENV(self):
        logger.warning("Not overriden")

    def run(self):
        logger.info(f"(command={self.command})")
        self._setReturnCode(-1)

        if not self.command:
            raise Exception(f"Command is empty")

        exe_filename = self.command[0]
        if not shutil.which(exe_filename):
            raise Exception(f"Executable not found at '{exe_filename}'")

        # process start callback
        self.start_callback()

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
                self.update_callback(message)

        logger.info(" ")
        logger.info("Waiting for Worker ...")
        worker.wait()
        logger.info("Worker TERMINATED")
        self._setReturnCode(worker.getReturnCode())

        # process finished
        self.finish_callback()

    def _setReturnCode(self, returncode: int):
        self.returncode = returncode

    def getReturnCode(self):
        return self.returncode

    def start(self, command: list):
        self.command = command
        self.run()
