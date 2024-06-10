# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import gzip
import os
from pathlib import Path
from xml.sax import parse

from gnucash.file.xml_extractor import MyHandler
from gnucash.data_model import GNU_FIELD_MEMO, GNU_FIELD_ACCOUNT_NAME, GNU_FIELD_ACC_TYPE, GNU_FIELD_DATE
from gnucash.data_model import GNU_FIELD_DESCRIPTION, GNU_FIELD_NUM, GNU_FIELD_RECONCILED_STATE
from gnucash.data_model import GNU_FIELD_TRANSACION_CURRENCY, GNU_FIELD_ACCOUNT_CURRENCY
from gnucash.data_model import GNU_FIELD_TRN_ID, GNU_FIELD_VALUE, GNU_FIELD_ATTRIBUTES_CONTAINER
from gnucash.data_model import gnu_extracted_columns


def extract_gnu_transactions(xml_file_name: Path, save_unused_tags: bool = False) -> list:
    xml_handler = MyHandler()
    parse(str(xml_file_name), xml_handler)

    collected_transactions = []
    for transaction in xml_handler.transactions:
        _r = _split_transaction(transaction, xml_handler.accounts)
        collected_transactions += [_r]

    gnu_records = []
    for transaction in collected_transactions:
        gnu_records += transaction

    if save_unused_tags:
        if len(xml_handler.unused) > 0:
            with open('unused_tags.txt', 'wt') as f:
                tags = sorted(xml_handler.unused)
                s = ';\n'.join(tags)
                f.write(s)

    return gnu_records


def _split_transaction(transaction, gnu_accounts):
    out = []
    for split in transaction.splits:
        account = gnu_accounts[split.acc]
        memo = split.memo if hasattr(split, GNU_FIELD_MEMO) else ''

        transaction_record = {
            GNU_FIELD_ACCOUNT_NAME: ':'.join(list_names(account, gnu_accounts)),
            GNU_FIELD_ACC_TYPE: account.type,
            GNU_FIELD_ACCOUNT_CURRENCY: account.account_currency,
            GNU_FIELD_DATE: transaction.date.partition(" ")[0],
            GNU_FIELD_DESCRIPTION: transaction.desc,
            GNU_FIELD_MEMO: memo,
            GNU_FIELD_NUM: transaction.num if hasattr(transaction, GNU_FIELD_NUM) else '',
            GNU_FIELD_RECONCILED_STATE: split.reconciled_state,
            GNU_FIELD_TRANSACION_CURRENCY: transaction.currency,
            GNU_FIELD_TRN_ID: transaction.trn_id,
            GNU_FIELD_VALUE: polynomial_to_float(split.val),
            GNU_FIELD_ATTRIBUTES_CONTAINER: memo + ' ' + transaction.desc
        }
        assert len(transaction_record) == len(gnu_extracted_columns)
        out += [transaction_record]
    return out


def list_names(the_account, accounts):
    if the_account.name == "Root Account":
        return []
    try:
        _acc = accounts[the_account.parent]
    except KeyError:
        print('{} account has no parent'.format(the_account.name))
        raise
    names = list_names(_acc, accounts) + [the_account.name]
    return names


def polynomial_to_float(x):
    up, slash, down = x.partition("/")
    return float(up) / float(down)


def _extract_gnucash_to_xml(gnu_file: Path) -> Path:
    xml_file_name = gnu_file.parent / f'{gnu_file.name[:-8]}.xml'

    with gzip.GzipFile(gnu_file, mode="r") as z:
        ret = z.read()

    with open(xml_file_name, "w+b") as xml_file:
        xml_file.write(ret)
    return xml_file_name


def extract_gnu_transactions_to_list(gnu_file: Path) -> list:
    assert isinstance(gnu_file, Path)
    xml_file_name = None
    try:
        xml_file_name = _extract_gnucash_to_xml(gnu_file)
        try:
            result = extract_gnu_transactions(xml_file_name, save_unused_tags=False)
        except KeyError:
            print(f'ERROR in {gnu_file}')
            raise

    finally:
        if xml_file_name:
            if os.path.isfile(xml_file_name):
                os.remove(xml_file_name)

    return result
