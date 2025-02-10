import subprocess

from multiprocessing import Queue, Lock

from PySide6.QtCore import QThread


class SubprocessWorker(QThread):

    def __init__(self, command: list, queue: Queue, env: dict | None = None):
        super().__init__()
        self.command = command
        self.queue = queue
        self.env = env

        self.lock = Lock()
        self.returncode = -1

    def _setReturnCode(self, returncode: int):
        with self.lock:
            self.returncode = returncode

    def getReturnCode(self):
        with self.lock:
            return self.returncode

    def run(self):
        try:
            cmd_str = ' '.join(self.command)
            self.queue.put(f"Starting process: \"{cmd_str}\"")

            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=self.env
            )

            while True:
                stdout = process.stdout
                output = stdout.readline() if stdout else ''
                retcode = process.poll()
                if output == "" and retcode is not None:
                    break
                if output:
                    self.queue.put(output.strip())  # Emit output
        except Exception as e:
            self.queue.put(f"Error: {e}")
        finally:
            self._setReturnCode(process.returncode)
            self.queue.put(" ")
            self.queue.put("Process TERMINATED")
            self.queue.put(f"Return code: {process.returncode}")
