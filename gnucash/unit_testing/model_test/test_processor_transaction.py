# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import unittest
from pathlib import Path

from gnucash.model.xml_processor import GnuCashXmlProcessor
from gnucash.model.transaction_descriptor import create_transaction


class TransactionGeneratorTester(unittest.TestCase):
    def test_add_transaction_and_inject_into_gnu(self, **kwargs):
        p = Path(__file__).parent
        input_file = p / 'GPM-20190126-2221.gnucash'
        output_file = p / 'GPM-20190126-2221_ADD.gnucash'

        descriptor = {
            'date': '2018-12-14',
            'description': '$ 771/2018 @RZR@ %Umowa licencyjna aSISt nr AS/2018/RZR% 1/3 czesci za licencje - rozlicz',
            'debit_acc': 'Aktywa:PLN:CA-BANK:BIEŻĄCY',
            'credit_acc': 'Rozliczenia:PLN:Należności:11',
            'amount': '123456.78'
        }
        gnucash_proc = GnuCashXmlProcessor(input_file)
        gnucash_proc.read_gnu_model(**kwargs)
        if output_file.is_file():
            output_file.unlink()

        transaction = create_transaction(input_file, descriptor)

        gnucash_proc.add_transactions(transaction)

        self.assertTrue(input_file.is_file())
        self.assertTrue(output_file.is_file())


if __name__ == '__main__':
    unittest.main()
