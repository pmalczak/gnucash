# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
from xml.etree.cElementTree import Element
from gnu_model.transaction import Transaction
from gnu_cash.file.account_solver import GnuAccountsSolver
from gnu_cash.guid import new_guid, new_guid5


def create_transaction(gnucash_file, descriptor):
    assert isinstance(descriptor, dict)
    assert len(descriptor) == 5

    account_solver = GnuAccountsSolver(gnucash_file=gnucash_file)
    td = TransactionDescriptor(account_solver, descriptor)
    transaction = td.as_transaction()
    return transaction


class TransactionDescriptor:
    def __init__(self, account_solver, descriptor):
        self.account_solver = account_solver
        assert isinstance(account_solver, GnuAccountsSolver)

        self._descriptor = self._init_descriptor_(descriptor)

    def as_str(self):
        return self._as_to_str(self._descriptor, '')

    def as_transaction(self):
        assert isinstance(self._descriptor, dict)
        assert len(self._descriptor) == 8

        e = Element('root')
        e.tail = '\n'
        result = Transaction(None, e, self._descriptor, logger=None)
        return result

    def _as_to_str(self, item, shift):
        assert isinstance(item, dict)

        result = ''

        for k, v in item.items():
            if isinstance(v, dict):
                result += '{}{} :\n'.format(shift, k)
                result += self._as_to_str(v, shift + '    ')
            elif isinstance(v, list):
                for item_ in v:
                    result += '{}{} : *\n'.format(shift, k)
                    result += self._as_to_str(item_, shift + '     ')
            else:
                result += '{}{} : {}\n'.format(shift, k, str(v))
        return result

    def _init_descriptor_(self, desc_in):
        assert isinstance(desc_in, dict)

        _amount = desc_in['amount']
        _splitted_amount = _amount.split('.')
        if len(_splitted_amount) > 1:
            assert len(_splitted_amount[1]) == 2
            amount = ( int(_splitted_amount[0]) * 100) + int(_splitted_amount[1])
        else:
            raise NotImplementedError

        amount_positive = '{}/100'.format(amount)
        amount_negative = '{}/100'.format(-amount)

        split_1 = {
            'id': new_guid().value,
            'reconciled-state': 'n',
            'account': self.account_solver.get_guid_by_account(desc_in['debit_acc']),
            'quantity': amount_positive,
            'value': amount_positive,
        }
        split_2 = {
            'id': new_guid().value,
            'reconciled-state': 'n',
            'account': self.account_solver.get_guid_by_account(desc_in['credit_acc']),
            'quantity': amount_negative,
            'value': amount_negative,
        }

        t = {
            'id': new_guid5(desc_in['description']).value,
            'currency': {
                'id': 'PLN',
                'space': 'ISO4217'},
            'num': '<*>',

            'date-posted': {'date': '2018-12-14 15:44:09.000000'},
            'date-entered': {'date': '2018-12-14 15:43:42.000000'},
            'description': desc_in['description'],

            'slots': [
                {'key': 'date-posted', 'gdate-value': {'gdate': desc_in['date']}}, ],
            'splits': [
                split_1,
                split_2, ],
        }
        return t
