#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Piotr.Malczak@gpm-sys.com'

from xml.etree.cElementTree import register_namespace


class GnuNameSpaces:
    name_spaces = {
        'gnc': 'http://www.gnucash.org/XML/gnc',
        'act': 'http://www.gnucash.org/XML/act',
        'book': 'http://www.gnucash.org/XML/book',
        'cd': 'http://www.gnucash.org/XML/cd',
        'cmdty': 'http://www.gnucash.org/XML/cmdty',
        'price': 'http://www.gnucash.org/XML/price',
        'slot': 'http://www.gnucash.org/XML/slot',
        'split': 'http://www.gnucash.org/XML/split',
        'sx': 'http://www.gnucash.org/XML/sx',
        'trn': 'http://www.gnucash.org/XML/trn',
        'ts': 'http://www.gnucash.org/XML/ts',
        'fs': 'http://www.gnucash.org/XML/fs',
        'bgt': 'http://www.gnucash.org/XML/bgt',
        'recurrence': 'http://www.gnucash.org/XML/recurrence',
        'lot': 'http://www.gnucash.org/XML/lot',
        'addr': 'http://www.gnucash.org/XML/addr',
        'owner': 'http://www.gnucash.org/XML/owner',
        'billterm': 'http://www.gnucash.org/XML/billterm',
        'bt-days': 'http://www.gnucash.org/XML/bt-days',
        'bt-prox': 'http://www.gnucash.org/XML/bt-prox',
        'cust': 'http://www.gnucash.org/XML/cust',
        'employee': 'http://www.gnucash.org/XML/employee',
        'entry': 'http://www.gnucash.org/XML/entry',
        'invoice': 'http://www.gnucash.org/XML/invoice',
        'job': 'http://www.gnucash.org/XML/job',
        'order': 'http://www.gnucash.org/XML/order',
        'taxtable': 'http://www.gnucash.org/XML/taxtable',
        'tte': 'http://www.gnucash.org/XML/tte',
        'vendor': 'http://www.gnucash.org/XML/vendor',

    }

    def __init__(self):
        for prefix, uri in self.name_spaces.items():
            register_namespace(prefix, uri)
