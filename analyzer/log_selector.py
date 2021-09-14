import datetime
import logging
import os
import re

from collections import namedtuple


class LogSelector:
    def __init__(self, path: str) -> None:
        self.logger = logging.getLogger(f'log_analyzer.Selector')
        self.path: str = path
        self.log_file: dict = {}
        self._pattern = re.compile(
            '(?P<year>20[0-9][0-9])'
            '(?P<month>[1-9]|1[0-2]|0[0-9])'
            '(?P<day>[1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])$'
        )

    def _check_path(self) -> bool:
        ret = False
        if not self.path:
            self.logger.error('log_dir directory not specified')
        elif not os.path.isdir(self.path):
            self.logger.error(f'log_dit {self.path} is not a directory')
        elif not os.path.exists(self.path):
            self.logger.error(f'log_dit {self.path} directory does not exist')
        else:
            ret = True

        return ret

    def _parse_date(self, text: str) -> datetime.date:
        res = self._pattern.search(text)
        if res:
            try:
                current_date = datetime.datetime.strptime(res.group(), '%Y%m%d').date()
                return current_date
            except ValueError:
                raise ValueError(f'strip time error in {res.group()}')
        else:
            raise ValueError(f'pattern search error in {text}')

    def __call__(self, *args, **kwargs) -> namedtuple:
        Log = namedtuple('log', 'path date gz_flag')

        if not self._check_path():
            return Log(None, None, None)

        log_path = None
        log_date: datetime.date = datetime.date(year=1900, month=1, day=1)
        log_gz_flag = None

        for root, _, files in os.walk(self.path):
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                if file_extension == '.gz':
                    file_name, file_extension = os.path.splitext(file_name)
                    gz_flag = True
                else:
                    gz_flag = False

                try:
                    current_date = self._parse_date(file_extension)
                except ValueError as e:
                    self.logger.error(e)
                    continue

                if log_date < current_date:
                    log_date, log_path, log_gz_flag = current_date, os.path.join(root, file), gz_flag
                elif log_date == current_date:
                    self.logger.error(f'found two log files with the same dates {log_path, os.path.join(root, file)}')
                    log_path = None
                    break

        if log_path is None:
            self.logger.error('log file not found')
            Log(None, None, None)

        self.logger.info(f'selected log file {log_path}')
        return Log(log_path, log_date, log_gz_flag)
