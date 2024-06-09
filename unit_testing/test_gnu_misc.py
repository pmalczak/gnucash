# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import unittest
from pathlib import Path

from unit_tests.obtain_test_data import TestFile


class FileNamesProviderTester(unittest.TestCase):

    def _test_proc(self, _core, _file):
        return

    def test_filenames_obj_creation_existing_target_dir(self):

        _core = 'GPM-20190819-2245'
        _file = Path(f'{_core}.gnucash')

        with TestFile(__file__, '../_test_data.zip') as tf:
            tf.clean_up((_file))
            tf.obtain(_file)

            try:
                self._test_proc(_core, _file)
            except Exception as e:
                raise
        return


if __name__ == '__main__':
    unittest.main()
