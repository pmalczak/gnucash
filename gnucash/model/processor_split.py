#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from gnu_model.account import Account
from gnu_model.xml_processor import GnuCashXmlProcessor
from gnu_model.transaction import Transaction
from app_logger.output_console import APP_TEXT_LOGGER

__author__ = 'Piotr.Malczak@gpm-sys.com'


def sale_transactions_selector(transaction, reversed_condition=None):
    assert isinstance(reversed_condition, bool)
    assert isinstance(transaction, Transaction)
    for split in transaction.splits.elements:
        if 'oot' in split.account.account_name:
            print('FOUND {}'.format(split.account.account_name))

    result = _sale_transactions_selector(transaction)
    return result if not reversed_condition else not result


def _sale_transactions_selector(transaction, excluded=None):
    assert isinstance(transaction, Transaction)
    splits = transaction.splits.elements

    for split in splits:
        account_name = split.account.account_name
        for item in excluded:
            if item in account_name:
                excluded[item]['transactions'] += 1
                return True
    return False


def sale_assignments_selector(account, reversed_condition=None):
    assert isinstance(reversed_condition, bool)
    if 'oot' in account.account_name:
        print('FOUND {}'.format(account.account_name))

    result = _sale_assignments_selector(account)
    return result if not reversed_condition else not result


def _sale_assignments_selector(account, excluded=None):
    assert isinstance(account, Account)
    if account.account_name:
        for item in excluded:
            if item in account.account_name:
                excluded[item]['assignments'] += 1
                return True
    return False


def create_excluded(splitted_year):
    _excluded = {
        'H# AKTYWA:%s' % splitted_year,
        'H# ROZLICZENIA:%s' % splitted_year,
        'H# VAT:%s' % splitted_year,
        'H# WYNIK:%s WYNIK' % splitted_year,
        'H# NIEPODATKOWE:%s' % splitted_year,
        'H# HR Rozliczenia:%s' % splitted_year,
        'H# HR WYNIK:%s' % splitted_year,
    }
    excluded = {}
    for item in _excluded:
        excluded[item] = {
            'assignments': 0,
            'transactions': 0,
        }
    return excluded


def split_book_by_year(splitted_year=None, **kwargs):
    assert isinstance(splitted_year, str) and len(splitted_year) == 4

    excluded = create_excluded(splitted_year)

    gnucash_proc = GnuCashXmlProcessor(**kwargs)

    fm = gnucash_proc.split_file_name('main')
    if os.path.isfile(fm):
        os.remove(fm)

    fs = gnucash_proc.split_file_name('splitted')
    if os.path.isfile(fs):
        os.remove(fs)

    gnucash_proc.read_gnu_model()
    gnucash_proc.split(selector, excluded=excluded)
    print(APP_TEXT_LOGGER.reset())


selector = {
    'transactions': sale_transactions_selector,
    'assignments': sale_assignments_selector,
}
