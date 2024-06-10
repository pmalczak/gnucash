# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

GNU_FIELD_ACCOUNT_NAME = 'acc_name'
GNU_FIELD_ACC_TYPE = 'acc_type'
GNU_FIELD_DATE = 'date'
GNU_FIELD_DESCRIPTION = 'desc'
GNU_FIELD_RECONCILED_STATE = 'reconciled_state'
GNU_FIELD_TRN_ID = 'trn_id'
GNU_FIELD_NUM = 'num'
GNU_FIELD_MEMO = 'memo'
GNU_FIELD_ACCOUNT_CURRENCY = 'account_currency'
GNU_FIELD_TRANSACION_CURRENCY = 'transaction_currency'
GNU_FIELD_VALUE = 'val'
GNU_FIELD_ATTRIBUTES_CONTAINER = 'attr_container'

gnu_extracted_columns = {
    GNU_FIELD_ACCOUNT_NAME,
    GNU_FIELD_ACC_TYPE,
    GNU_FIELD_ACCOUNT_CURRENCY,
    GNU_FIELD_DATE,
    GNU_FIELD_DESCRIPTION,
    GNU_FIELD_MEMO,
    GNU_FIELD_NUM,
    GNU_FIELD_RECONCILED_STATE,
    GNU_FIELD_TRANSACION_CURRENCY,
    GNU_FIELD_TRN_ID,
    GNU_FIELD_VALUE,
    GNU_FIELD_ATTRIBUTES_CONTAINER,
}
ACCOUNT_NAME = 'Account name'

ACCOUNT_TYPE = 'Account type'
GNU_ACC_TYPE_INCOME = 'INCOME'
GNU_ACC_TYPE_EXPENSE = 'EXPENSE'
GNU_ACC_TYPE_ASSET = 'ASSET'
GNU_ACC_TYPE_BANK = 'BANK'
GNU_ACC_TYPE_EQUITY = 'EQUITY'
GNU_ACC_TYPE_LIABILITY = 'LIABILITY'
GNU_ACC_TYPE_CASH = 'CASH'
GNU_ACC_TYPE_PAYABLE = 'PAYABLE'

DATE = 'DATE'
DESCRIPTION = 'Description'
VALUE = 'Value'
NUM = 'Num'
MEMO = 'Memo'
RECONCILED_STATE = 'reconciled_state'
TRN_ID = 'trn_id'

ACCOUNT_CURRENCY = 'account_currency'
TRANSACTION_CURRENCY = 'transaction_currency'

ALL_ACCOUNT_TYPES = (
    GNU_ACC_TYPE_ASSET,
    GNU_ACC_TYPE_BANK,
    GNU_ACC_TYPE_CASH,
    GNU_ACC_TYPE_EQUITY,
    GNU_ACC_TYPE_EXPENSE,

    GNU_ACC_TYPE_INCOME,
    GNU_ACC_TYPE_LIABILITY,
    GNU_ACC_TYPE_PAYABLE,
)
PL_ACCOUNT_TYPES = (
    GNU_ACC_TYPE_EXPENSE,
    GNU_ACC_TYPE_INCOME,
)