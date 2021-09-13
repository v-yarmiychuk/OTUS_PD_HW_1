# PYTHON_ARGCOMPLETE_OK
import argparse
import logging
import os

import argcomplete

import analyzer
from analyzer.configurator import Conf
from analyzer.log_selector import LogSelector
from analyzer.logger import log_format
from analyzer.logger import logger


class Arguments:
    def __init__(self):
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

    def parse(self):
        self.args = self.parser.parse_args()
        return self.args


def run():
    os.chdir(os.path.join(os.path.dirname(analyzer.__file__), os.path.pardir))

    logger.info('start log analyzer')

    args = Arguments().parse()
    conf = Conf(args.config)

    if conf.log_file_path:
        fh = logging.FileHandler(conf.log_file_path)
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    logger.info(args.config)
    logger.info(conf.config)

    log_selector = LogSelector(conf.log_dir)
    log_path, log_date, log_gz_fla = log_selector()


