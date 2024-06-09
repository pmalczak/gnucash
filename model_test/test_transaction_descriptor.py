# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import os
import unittest
from pathlib import Path

from unit_tests.obtain_test_data import TestFile
from gnu_model.transaction import Transaction
from gnu_model.transaction_descriptor import TransactionDescriptor, create_transaction
from gnu_cash.file.account_solver import GnuAccountsSolver, AccountDoesNotExist


def _get_simplified_transaction_descriptor():
    result = {
        'date': '2018-12-14',
        'description': '$ 771/2018 @RZR@ %Umowa licencyjna aSISt nr AS/2018/RZR% 1/3 czesci za licencje - rozlicz',
        'debit_acc': 'Aktywa:PLN:CA-BANK:BIEŻĄCY',
        'credit_acc': 'Rozliczenia:PLN:Należności:11',
        'amount': '123456.78'
    }
    return result


class TransactionGeneratorTester(unittest.TestCase):

    def test_generate_transaction_descriptor(self):
        input_name = Path('GPM-20190126-2221.gnucash')

        with TestFile(__file__, '_test_data.zip') as tf:
            tf.clean_up(input_name)
            tf.obtain(input_name)
            descriptor = _get_simplified_transaction_descriptor()

            input_file = Path().resolve() / input_name
            account_solver = GnuAccountsSolver(gnucash_file=input_file)
            tg = TransactionDescriptor(account_solver, descriptor)
            result = tg.as_str()
            print(result)

            self.assertTrue(len(tg._descriptor) == 8)
            self.assertTrue(isinstance(result, str))

            tf.clean_up(input_name)

    def test_generate_transaction(self):
        input_name = Path('SALE-20190124-2221.gnucash')

        with TestFile(__file__, '_test_data.zip') as tf:
            tf.clean_up(input_name)
            tf.obtain(input_name)

            input_file = Path().resolve() / input_name
            descriptor = _get_simplified_transaction_descriptor()
            transaction = create_transaction(input_file, descriptor)
            self.assertTrue(isinstance(transaction, Transaction))
            tf.clean_up(input_name)

    def test_generate_transaction_lacking_acc(self):
        input_name = Path('TST.gnucash')
        expected_raised_exception = True

        with TestFile(__file__, '_test_data.zip') as tf:
            tf.clean_up(input_name)
            tf.obtain(input_name)
            input_file = Path().resolve() / input_name

            assert os.path.isfile(input_file)

            try:
                account_solver = GnuAccountsSolver(gnucash_file=input_file)
                descriptor = _get_simplified_transaction_descriptor()

                tg = TransactionDescriptor(account_solver, descriptor)
                self.assertFalse(expected_raised_exception)
                result = tg.as_str()
                print(result)

            except AccountDoesNotExist as e:
                self.assertTrue(expected_raised_exception)

            # tf.clean_up(input_name)
        return


if __name__ == '__main__':

    unittest.main()
