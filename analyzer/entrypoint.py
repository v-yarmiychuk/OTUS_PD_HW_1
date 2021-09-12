# PYTHON_ARGCOMPLETE_OK

import argparse
import os

import argcomplete

import analyzer
from analyzer.configurator import Conf


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

    args = Arguments().parse()
    conf = Conf(args.config)
    print(args.config)
    print(conf.config)
