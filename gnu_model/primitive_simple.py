#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Piotr.Malczak@gpm-sys.com'

from gnu_model.xml_element import XmlElement


class TrnId(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}id', attrib={'type':'guid'})
        elem.tail = '\n '
        val = args
        assert isinstance(val, str)
        assert len(val) == 32
        elem.text = val
        return elem


class ActId(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/act}id', attrib={'type':'guid'})
        elem.tail = '\n  '

        assert isinstance(args, str)
        assert len(args) == 32
        elem.text = args
        return elem


class CmdtyId(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/cmdty}id')
        elem.tail = '\n '

        assert isinstance(args, str)
        assert len(args) == 3
        elem.text = args
        return elem


class SplitId(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}id', attrib={'type':'guid'})
        elem.tail = '\n '

        assert isinstance(args, str)
        assert len(args) == 32
        elem.text = args
        return elem


class Space(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/cmdty}space')
        elem.tail = '\n '

        assert isinstance(args, str)
        assert args in ('ISO4217', )
        elem.text = args
        return elem


class Quantity(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}quantity')
        elem.tail = '\n '

        assert isinstance(args, str)
        assert len(args.split('/')) == 2
        elem.text = args
        return elem


class Num(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}num')
        elem.tail = '\n '
        elem.text = args
        return elem


class Memo(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}memo')
        elem.tail = '\n '
        assert isinstance(args, str)
        elem.text = args
        return elem


class Date(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/ts}date')
        elem.tail = '\n '
        assert isinstance(args, str)
        if len(args) != 26:
            print('len(date)=', len(args))
        elem.text = args
        return elem


class AccountDescription(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/act}description')
        elem.tail = '\n '

        assert isinstance(args, str)
        elem.text = args
        return elem


class TransactionDescription(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}description')
        elem.tail = '\n '

        assert isinstance(args, str)
        elem.text = args
        return elem


class AccountKey(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)
        if elem_self is not None:
            if elem_self.text not in ('color',
                                      'placeholder',
                                      'reconcile-info',
                                      'include-children',
                                      'last-date',
                                      'last-interval',
                                      'days',
                                      'months',
                                      'auto-interest-transfer',
                                      'postpone',
                                      'balance',
                                      'date',
                                      ):
                raise Exception(elem_self.text)
        return

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/slot}key')
        elem.tail = '\n '
        elem.text = args
        return elem


class TransactonKey(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)
        if elem_self is not None:
            if elem_self.text not in ('date-posted',
                                      'notes',
                                      'reversed-by',
                                      'assoc_uri',
                                      ):
                raise Exception(elem_self.text)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/slot}key')
        elem.tail = '\n '
        elem.text = args
        return elem


class Value(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}value')
        elem.tail = '\n '

        assert isinstance(args, str)
        assert len(args.split('/')) == 2
        elem.text = args
        return elem


class Action(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}action')
        elem.tail = '\n '
        elem.text = args  # zwykle 126,96
        return elem


class SplitAccount(XmlElement):  # SplitAccount
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        self.account_name = None
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        if 'accounts_name_decoder' in kwargs:
            decoder = kwargs['accounts_name_decoder']
            self.account_name = decoder(self.text)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}account', attrib={'type':'guid'})
        elem.tail = '\n '

        assert len(args) == 32
        elem.text = args
        return elem


class ReconciledState(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)
        if elem_self:
            assert elem_self.text in ('n', 'y', 'c')

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/split}reconciled-state')
        elem.tail = '\n '

        assert args in ('n', 'y', 'c')
        elem.text = args
        return elem


class Name(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)


class Type(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)


class CommodityScu(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)


class GDate(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, 'gdate')
        elem.tail = '\n '

        elem.text = args
        return elem

class CountData(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)


class Parent(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().__init__(elem_self, parent, args, **kwargs)
