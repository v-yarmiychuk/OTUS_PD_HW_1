import hashlib
import json
import os
import unittest

from analyzer.log_parser import LogParser
from analyzer.log_selector import LogSelector
from analyzer.report_generator import ReportGenerator
from test.bace_class import BaseTestClass


class TestLogSelector(BaseTestClass):
    @staticmethod
    def getMd5(file_path):
        m = hashlib.md5()
        with open(file_path, 'rb') as f:
            line = f.read()
            m.update(line)
        md5code = m.hexdigest()
        return md5code

    def test_report_generator(self):
        log = LogSelector(self.directory_1)()
        log_data = LogParser(log.path, log.gz_flag)()

        report_path = os.path.join(self.directory_1, f'report_{log.date.strftime("%d_%m_%Y")}.html')

        ReportGenerator(
            template_path='./templates/report.html',
            report_path=report_path,
            report_data={'table_json': json.dumps(log_data)}
        )(overwrite=False)

        self.assertTrue(
            os.path.exists(report_path)
        )

        with self.assertRaises(Exception):
            ReportGenerator(
                template_path='./templates/report.html',
                report_path=report_path,
                report_data={'table_json': json.dumps(log_data)}
            )(overwrite=False)

        self.assertTrue(self.getMd5(report_path) == 'ea1f24509e9aea9a27150dfedc86124e')


if __name__ == '__main__':
    unittest.main()
