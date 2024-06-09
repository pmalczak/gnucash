# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import unittest
from pathlib import Path

from unit_tests.obtain_test_data import TestFile
from gnucash.extract_gnu_transactions import extract_gnu_transactions_to_list


class Tester(unittest.TestCase):

    def test_extracting_to_list(self):
        base = 'GPM-20190828-0839'
        gnu_file_name = Path('%s.gnucash' % base)

        with TestFile(__file__, test_file='test_gnu_importer_data.zip') as tf:
            tf.clean_up(['*.gnucash', '*.xml', '*.xlsx'])
            tf.obtain(gnu_file_name)
            transactions = extract_gnu_transactions_to_list(gnu_file_name)
            self.assertTrue(len(transactions) == 30828)
        return


if __name__ == '__main__':
    unittest.main()
