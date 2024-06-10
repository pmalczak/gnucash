# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from gnucash.model.xml_element import XmlElement, extract_name_space
from gnucash.model import primitive_pair as pair
from gnucash.model import primitive_composite as composite


class Splits(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('split', )
        self.elements = []
        XmlElement.__init__(self, elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)

            if tag == 'split':
                self.elements += [composite.Split(elem, None, None, **kwargs)]
            else:
                raise NotImplementedError

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}splits')
        elem.tail = '\n '
        elem.text = '\n '

        assert isinstance(args, (tuple, list))
        for item in args:
            _e = composite.Split(None, elem, item, **kwargs)
            self.elements += [_e]
        return elem


class TransactionSlots(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        self.elements = []
        XmlElement.__init__(self, elem_self, parent, args, **kwargs)

    def retrieve(self, **kwarg):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)

            if tag == 'slot':
                self.elements += [pair.TransactionSlot(elem, None, None, **kwarg)]
            else:
                raise NotImplementedError

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}slots')
        elem.tail = '\n '
        elem.text = '\n  '

        for item in args:
            self.elements += [pair.TransactionSlot(None, elem, item, **kwargs)]
        return elem


class AccountSlots(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        self.elements = []
        XmlElement.__init__(self, elem_self, parent, args, **kwargs)

    def __str__(self):
        result = ', '.join(self.elements)
        return result

    def retrieve(self, **kwarg):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)

            if tag == 'slot':
                self.elements += [pair.AccountSlot(elem, None, None, **kwarg)]
            else:
                raise NotImplementedError
        return

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/act}slots')
        elem.tail = '\n '
        elem.text = '\n  '

        for item in args:
            self.elements += [pair.AccountSlot(None, elem, item, **kwargs)]
        return elem

    def add_account_slot(self, account_slot):
        assert isinstance(account_slot, pair.AccountSlot)

        x = self.find(account_slot)
        if x is None:
            self._elem_self.append(account_slot._elem_self)
            self.elements += [account_slot]
        return

    def __contains__(self, item):
        if not isinstance(item, pair.AccountSlot):
            raise TypeError
        x = item.key.text
        for item in self.elements:
            if item.text == x:
                return True
        return False

    def find(self, item):
        if not isinstance(item, pair.AccountSlot):
            raise TypeError
        x = item.key.text
        for item in self.elements:
            if item.text == x:
                return item
        return None
