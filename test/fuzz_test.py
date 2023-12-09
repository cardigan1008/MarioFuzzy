import unittest
from unittest.mock import patch

from action.fuzz import Fuzz
from action.fuzz import read_file_content


class TestFuzzMethods(unittest.TestCase):
    @patch('builtins.open', return_value=unittest.mock.mock_open(read_data='abcd').return_value)
    def test_read_file_content(self, mock_open):
        target_path = "product/seed/seed1.txt"
        content = read_file_content(target_path)

        self.assertEqual(content, 'abcd')


if __name__ == '__main__':
    unittest.main()
