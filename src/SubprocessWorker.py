import sys
import os
import subprocess

from multiprocessing import Queue

from PyQt5.QtCore import QThread


class SubprocessWorker(QThread):

    def __init__(self, command: list, queue: Queue, env: dict = None):
        super().__init__()
        self.command = command
        self.queue = queue
        self.env = env

    def run(self):
        try:
            cmd_str = ' '.join(self.command)
            self.queue.put(f"Running: \"{cmd_str}\"")

            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=self.env
            )

            while True:
                output = process.stdout.readline()
                retcode = process.poll()
                if output == "" and retcode is not None:
                    break
                if output:
                    self.queue.put(output.strip())  # Emit output

            self.queue.put(" ")
            self.queue.put("Process TERMINATED")
            self.queue.put(f"Return code: {process.returncode}")
        except Exception as e:
            self.queue.put(f"Error: {e}")
