"""
    Unit test for Parallel Coordinates
    author: Juan L. Onieva

    TODO: Complete the unit test for the class ir order to reduce the number of failures!
"""

import unittest
from ParallelCoordinates import ParallelCoordinates

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.my_pc = ParallelCoordinates(file_name='data/iris.csv', header='infer')

    def test_read_file_should_detect_when_header_is_not_infer_or_none(self):
        """
        Detect if the header is 'infer' or 'None'
        :return:
        """
        with self.assertRaises(Exception):
            self.my_pc.read_file(file_name='file-name', header='other', my_delimiter=',')

    def test_read_file_should_detect_when_header_is_not_infer_or_none(self):
        """
        Detect if the file exists
        :return:
        """
        with self.assertRaises(IOError):
            self.my_pc.read_file(file_name='file-name-not-exist', header='other', my_delimiter=',')

    def test_after_normalize_total_must_be_ont(self):
        """
        Check that the function normalize works properly
        :return:
        """
        result = 0
        for col in self.my_pc.my_df_normalize.columns:
            result = result + sum(self.my_pc.my_df_normalize[col])
        expected_result = 1
        result = result/len(self.my_pc.my_df_normalize.columns)
        self.assertEqual(expected_result, result)

    def test_path_add_at_the_end_the_default_directory_results(self):
        result = self.my_pc.my_path()
        result = result.split('/')
        result = result[-1]
        expected_string = 'results'
        self.assertEqual(expected_string, result)


if __name__ == '__main__':
    unittest.main()
