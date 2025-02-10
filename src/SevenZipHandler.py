import logging

from utils.Regex import Regex

from utils.SubprocessHandler import SubprocessHandler

# Create a logger for this module
logger = logging.getLogger(__name__)


class SevenZipHandler(SubprocessHandler):
    @staticmethod
    def _decode_file_format_arg(filename: str):
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

    def __init__(self, start_callback, update_callback, finish_callback, env: dict):
        super().__init__(start_callback, update_callback, finish_callback, env=env)
        self.addUpdateCallback(self._check_progress)

    def _check_progress(self, message):
        try:
            # Search for progress percentage in the message using the regex pattern
            # (e.g., "Extracting: 23%")
            regex = Regex(r"(Compressing|Extracting).*\s(\d+)%")
            match = regex.search(message)
            # Extract progress
            _, progress = match.groups()
            self.progress.emit(int(progress))
        except Exception as e:
            pass

    def startCompress(self, input_files: list, output_file: str, extra_args: str = ''):
        extra_args_list = extra_args.split()
        extra_args_list.append(self._decode_file_format_arg(output_file))

        command = [self.env['7ZIP']]
        command += ["a"] + extra_args_list
        command += [output_file] + input_files

        self.start(command)

    def startDecompress(self, input_file: str, output_dir: str, extra_args: str = ''):
        extra_args_list = extra_args.split()
        extra_args_list.append(self._decode_file_format_arg(input_file))

        command = [self.env['7ZIP']]
        command += ["x", input_file]
        command += [f"-o{output_dir}"]
        command += extra_args_list

        self.start(command)
