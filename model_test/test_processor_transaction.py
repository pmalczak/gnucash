# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import os
import unittest
from pathlib import Path
from unit_tests.obtain_test_data import TestFile

from gnu_model.xml_processor import GnuCashXmlProcessor
from gnu_model.transaction_descriptor import create_transaction


class TransactionGeneratorTester(unittest.TestCase):
    def test_add_transaction_and_inject_into_gnu(self, **kwargs):
        core = 'GPM-20190126-2221'
        input = Path(f'{core}.gnucash')
        output = Path(f'{core}_ADD.gnucash')

        with TestFile(__file__, '_test_data.zip') as tf:
            descriptor = {
                'date': '2018-12-14',
                'description': '$ 771/2018 @RZR@ %Umowa licencyjna aSISt nr AS/2018/RZR% 1/3 czesci za licencje - rozlicz',
                'debit_acc': 'Aktywa:PLN:CA-BANK:BIEŻĄCY',
                'credit_acc': 'Rozliczenia:PLN:Należności:11',
                'amount': '123456.78'
            }

            tf.clean_up((input, output))
            tf.obtain(input)

            input_file = Path().resolve() / input
            gnucash_proc = GnuCashXmlProcessor(input_file)
            gnucash_proc.read_gnu_model(**kwargs)
            self.assertFalse(os.path.isfile(output))

            transaction = create_transaction(input_file, descriptor)

            gnucash_proc.add_transactions(transaction)

            self.assertTrue(os.path.isfile(input))
            self.assertTrue(os.path.isfile(output))

            tf.clean_up(input)


if __name__ == '__main__':
    unittest.main()
