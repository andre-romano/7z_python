
import sys
import os
import subprocess

from multiprocessing import Process, Queue, Lock


class SubprocessWorker(Process):
    def __init__(self, command: list, queue: Queue, lock, env: dict = None):
        super().__init__()
        self.command = command
        self.queue = queue
        self.lock = lock
        self.env = env

    def run(self):
        try:
            cmd_str = ' '.join(self.command)
            self.queue.put(f"\"{cmd_str}\"")
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=self.env
            )
            retcode = None
            while True:
                output = process.stdout.readline()
                retcode = process.poll()
                if output == "" and retcode is not None:
                    break
                if output:
                    self.queue.put(output.strip())  # Send output to the queue
            self.queue.put(f" ")
            self.queue.put(f"Process TERMINATED")
            self.queue.put(f"Return code: {retcode}")
        except Exception as e:
            self.queue.put(f"Error: {e}")
