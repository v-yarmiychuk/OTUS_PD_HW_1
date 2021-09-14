import logging
import os
from pathlib import Path
from string import Template


class ReportGenerator:
    def __init__(self, template_path: str, report_path: str, report_data: dict) -> None:
        self.logger = logging.getLogger(f'log_analyzer.ReportGenerator')
        self.template_path = template_path
        self.report_path = report_path
        self.report_data = report_data

    def __call__(self, overwrite: bool = True, *args, **kwargs):
        Path(os.path.dirname(self.template_path)).mkdir(parents=True, exist_ok=True)
        Path(os.path.dirname(self.report_path)).mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.report_path) and not overwrite:
            raise Exception('the report file already exists')

        with open(self.template_path, mode="rt") as f:
            report = Template(f.read()).safe_substitute(self.report_data)

        with open(self.report_path, mode="wt") as f:
            f.write(report)
