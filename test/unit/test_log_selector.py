import os
import shutil
import unittest

from analyzer.log_selector import LogSelector
from test.bace_class import BaseTestClass


class TestLogSelector(BaseTestClass):
    def test_select_log(self):
        log = LogSelector(self.directory_1)()
        self.assertTrue(log.path == self.file_3)

        os.remove(self.file_3)
        log = LogSelector(self.directory_1)()
        self.assertTrue(log.path == self.file_2)

        os.remove(self.file_2)
        log = LogSelector(self.directory_1)()
        self.assertTrue(log.path == self.file_1)

    def test_select_log_not_unique(self):
        self.file_4 = os.path.join(self.directory_1, self.file_3_name)
        shutil.copyfile(self.sample_data, self.file_4)

        with self.assertRaises(Exception):
            LogSelector(self.directory_1)()


if __name__ == '__main__':
    unittest.main()
