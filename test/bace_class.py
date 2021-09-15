import os
import shutil
import tempfile
import unittest


class BaseTestClass(unittest.TestCase):
    sample_data = './test/sample_data'

    def setUp(self) -> None:
        self.directory_1 = tempfile.mkdtemp()
        self.directory_2 = tempfile.mkdtemp(dir=self.directory_1)
        self.directory_3 = tempfile.mkdtemp(dir=self.directory_2)

        self.file_1_name = 'nginx-access-ui.log-20190625'
        self.file_2_name = 'nginx-access-ui.log-20190725'
        self.file_3_name = 'nginx-access-ui.log-20190730'

        self.file_1 = os.path.join(self.directory_1, self.file_1_name)
        self.file_2 = os.path.join(self.directory_2, self.file_2_name)
        self.file_3 = os.path.join(self.directory_3, self.file_3_name)

        shutil.copyfile(self.sample_data, self.file_1)
        shutil.copyfile(self.sample_data, self.file_2)
        shutil.copyfile(self.sample_data, self.file_3)

    def tearDown(self):
        shutil.rmtree(self.directory_1)
