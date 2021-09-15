import unittest

from analyzer.log_parser import LogParser
from analyzer.log_selector import LogSelector
from test.bace_class import BaseTestClass


class TestLogSelector(BaseTestClass):
    def test_parser(self):
        log = LogSelector(self.directory_1)()
        log_data = LogParser(log.path, log.gz_flag)()
        self.assertTrue(len(log_data) == 764)

        log_data = sorted(log_data, key=lambda k: k['count'], reverse=True)

        self.assertTrue(
            log_data[0] == {'url': '/export/appinstall_raw/2017-06-30/ ',
                            'count': 88,
                            'count_perc': 8.8,
                            'time_sum': 0.23000000000000018,
                            'time_perc': 0.04622641699041924,
                            'time_avg': 0.0026136363636363657,
                            'time_max': 0.006,
                            'time_med': 0.0025}
        )


if __name__ == '__main__':
    unittest.main()
