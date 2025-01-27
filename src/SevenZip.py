import logging
import sys
import os

from multiprocessing import Queue

from Regex import Regex
from SubprocessWorker import SubprocessWorker

# Create a logger for this module
logger = logging.getLogger(__name__)


class SevenZip:
    @staticmethod
    def decode_file_format_arg(filename: str):
        file_fmt_arg = '-t'
        try:
            file_format = Regex(
                r"\.([^\.]+)$").search(filename).groups()[0]
            if file_format in ('7z', 'zip', 'tar', 'xz', 'lzma', 'lzma2', 'zst', 'cab', 'wim', 'iso'):
                file_fmt_arg += file_format
            elif file_format in ('gz'):
                file_fmt_arg += 'gzip'  # .tar.gz
            elif file_format in ('bz2'):
                file_fmt_arg += 'bzip2'  # .tar.bz2
            else:
                raise Exception(
                    f"decode_file_format_arg() : File format not detected for {filename}")
        except Exception as e:
            logger.error(f"{e}")
            return ''
        return file_fmt_arg

    def __init__(self, env, start_callback, update_callback, finish_callback):
        super().__init__()

        self._setENV(env)

        self.start_callback = start_callback
        self.update_callback = update_callback
        self.finish_callback = finish_callback

        self.arguments = []

    def _setENV(self, env: dict):
        self.env = env

        self.env['7ZIP_BIN'] = f"{self.env['DATA_PATH']}{os.path.sep}lib"
        self.env['7ZIP'] = f"{self.env['7ZIP_BIN']}{os.path.sep}7z.exe"

        logger.debug(f"env['7ZIP_BIN']={self.env['7ZIP_BIN']}")
        logger.debug(f"env['7ZIP']={self.env['7ZIP']}")

    def run(self):
        sevenZip_exe = self.env['7ZIP']
        command = [sevenZip_exe] + self.arguments
        logger.info(f"(command={command})")
        if not os.path.isfile(sevenZip_exe):
            raise Exception(f"7-Zip not found at '{sevenZip_exe}'")

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
