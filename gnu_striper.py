# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from pathlib import Path

from gnu_model.xml_processor import GnuCashXmlProcessor
from gnu_cash.gnu_file_operations import GnuFileOperations
from gnu_cash.gnu_file_locks import GnuFileLocks
from app_logger.output_console import APP_TEXT_LOGGER

from gnu_model.account import Account
from gnu_model.transaction import Transaction


def is_item_in_account_name(item, account):
    return item in account.account_name


def is_item_not_in_account_name(item, account):
    return item not in account.account_name


def _create_exclusions(_excluded):
    excluded = {}
    for item in _excluded:
        excluded[item] = {
            'assignments': 0,
            'transactions': 0,
        }
    return excluded


def transactions_selector(transaction, test_account, excluded):
    assert isinstance(transaction, Transaction)
    splits = transaction.splits.elements

    for split in splits:
        account = split.account
        for item in excluded:
            if test_account(item, account):
                excluded[item]['transactions'] += 1
                return True
    return False


def accounts_selector(account: Account, test_assignment, excluded) -> bool:
    assert isinstance(account, Account)
    if account.account_name:
        for item in excluded:
            if test_assignment(item, account):
                excluded[item]['assignments'] += 1
                return True
    return False


def strip_transactions(gnucash_file_p, selector, _excluded: set, new_file_name_proc, **kwargs):
    assert isinstance(_excluded, set)
    excluded = _create_exclusions(_excluded)
    processed = remove_pd_transactions(gnucash_file_p,
                                       new_file_name_proc,
                                       selector=selector,
                                       excluded=excluded,
                                       **kwargs
                                       )
    if processed:
        GnuFileOperations(gnucash_file_p).copy_to_backup()

        APP_TEXT_LOGGER.log(str(gnucash_file_p))
        APP_TEXT_LOGGER.log('account name            transactions   assignments')
        for k, v in excluded.items():
            s = '{:<20}           {:>5}         {:>5}'.format(k, v['transactions'], v['assignments'])
            APP_TEXT_LOGGER.log(s)
    return


def remove_pd_transactions(gnucash_file: Path, file_name_procedure, **kwargs) -> Path:
    lock = GnuFileLocks(gnucash_file)
    lock.obtain_lock()
    operations = GnuFileOperations(gnucash_file)

    try:
        gnucash_file_out = file_name_procedure(gnucash_file, **kwargs)
        gnucash_processor = GnuCashXmlProcessor(gnucash_file)
        new_gnucash_file = gnucash_processor.remove_records(gnucash_file_out, **kwargs)

    finally:
        lock.release_lock()
        operations.remove_backup_directory_if_empty()

    return new_gnucash_file
