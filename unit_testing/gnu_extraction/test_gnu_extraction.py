# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import unittest
from pathlib import Path

from extract_gnu_transactions import extract_gnu_transactions_to_list


class Tester(unittest.TestCase):

    def test_extracting_to_list(self):
        gnu_file_name = Path('GPM-20190828-0839.gnucash')
        transactions = extract_gnu_transactions_to_list(gnu_file_name)
        self.assertTrue(len(transactions) == 30828)

        return


if __name__ == '__main__':
    unittest.main()
