import logging
import sys
import os

from multiprocessing import Queue

from SubprocessWorker import SubprocessWorker

# Create a logger for this module
logger = logging.getLogger(__name__)


class SevenZip:
    def __init__(self, data_path, start_callback, update_callback, finish_callback):
        super().__init__()

        self.data_path = data_path
        self.lib_path = f"{data_path}{os.path.sep}lib"

        self.start_callback = start_callback
        self.update_callback = update_callback
        self.finish_callback = finish_callback

        self.arguments = []

        self._setENV()

    def _setENV(self):
        self.env = os.environ.copy()
        self.env['LANG'] = 'en'
        self.env['7ZIP_BIN'] = f"{self.lib_path}"
        self.env['7ZIP'] = f"{self.env['7ZIP_BIN']}{os.path.sep}7z.exe"

        logger.debug(f"env['7ZIP_BIN']={self.env['7ZIP_BIN']}")
        logger.debug(f"env['7ZIP']={self.env['7ZIP']}")
        logger.debug(f"env['LANG']={self.env['LANG']}")

    def run(self):
        sevenZip_exe = self.env['7ZIP']
        command = [sevenZip_exe] + self.arguments
        logger.info(f"(command={command})")
        if not os.path.isfile(sevenZip_exe):
            raise Exception(
                f"7-Zip not found. PATH={os.environ.get('PATH')}")

        # process start callback
        self.start_callback()

        # create queue
        queue = Queue()

        # Start the worker process
        logger.info("Starting worker ...")
        worker = SubprocessWorker(command, queue, env=self.env)
        worker.start()

        # Process the output from the worker process
        self._handle_output(queue, worker)

    def _handle_output(self, queue: Queue, worker: SubprocessWorker):
        # Process the queue's output in the main thread
        while worker.isRunning():
            while not queue.empty():
                message = queue.get()
                self.update_callback(message)

        logger.info("Waiting for Worker ...")
        worker.wait()
        logger.info("Worker TERMINATED")

        # process finished
        self.finish_callback()

    def start(self, arguments: list):
        self.arguments = arguments
        self.run()
