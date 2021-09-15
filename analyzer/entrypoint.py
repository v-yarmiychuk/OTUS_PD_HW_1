# PYTHON_ARGCOMPLETE_OK
import argparse
import json
import logging
import os
from typing import Any

import argcomplete

import analyzer
from analyzer.configurator import Conf
from analyzer.log_parser import LogParser
from analyzer.log_selector import LogSelector
from analyzer.logger import log_format
from analyzer.logger import logger
from analyzer.report_generator import ReportGenerator


class Arguments:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description='training log parser')
        self.parser.add_argument(
            '--config',
            required=False,
            type=argparse.FileType(),
            help='point to overriding config file', )

        argcomplete.autocomplete(self.parser)
        self.args = None
        self.parser.parse_args()

    def parse(self) -> Any:
        self.args = self.parser.parse_args()
        return self.args


def run_() -> None:
    os.chdir(os.path.join(os.path.dirname(analyzer.__file__), os.path.pardir))
    args = Arguments().parse()
    conf = Conf(args.config)

    if conf.log_file_path:
        fh = logging.FileHandler(conf.log_file_path)
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    logger.info('start log analyzer')
    log = LogSelector(conf.log_dir)()
    log_data = LogParser(log.path, log.gz_flag)()
    log_data = sorted(log_data, key=lambda k: k['count'], reverse=True)
    log_data = log_data[0:conf.report_size]
    ReportGenerator(
        template_path='./templates/report.html',
        report_path=os.path.join(conf.report_dir, f'report_{log.date.strftime("%d_%m_%Y")}.html'),
        report_data={'table_json': json.dumps(log_data)}
    )(overwrite=True)


def run() -> None:
    try:
        run_()
    except BaseException as e:
        logger.exception(e)
        raise e
