#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import Element
from gnu_model.xml_element import XmlElement, extract_name_space
from gnu_model.transaction import Transaction
from gnu_model.account import Account

__author__ = 'Piotr.Malczak@gpm-sys.com'


class Book(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('id', )
        self.elements = {
            'assignments'    : [],
            'transactions': []
        }

        XmlElement.__init__(self, elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)

            if tag == 'id':
                # self.elements += []
                pass
            elif tag == 'slots':
                pass
                #self.elements += []
            elif tag == 'count-data':
                pass
                #self.elements += []
            elif tag == 'commodity':
                pass
                #self.elements += []
            elif tag == 'pricedb':
                pass
                #self.elements += []
            elif tag == 'account':
                self.elements['assignments']     += [Account(elem, None, None, **kwargs)]
            elif tag == 'transaction':
                self.elements['transactions'] += [Transaction(elem, None, None, **kwargs)]
            elif tag == 'budget':
                pass
                #self.elements += []
            elif tag == 'GncBillTerm':
                pass
                #self.elements += []
            elif tag == 'GncCustomer':
                pass
                #self.elements += []
            elif tag == 'GncEmployee':
                pass
                #self.elements += []
            elif tag == 'GncInvoice':
                pass
                #self.elements += []
            elif tag == 'GncTaxTable':
                pass
                #self.elements += []
            elif tag == 'GncVendor':
                pass
                #self.elements += []

            else:
                raise NotImplementedError

    def select_components(self, book_component, selector, **kwargs):
        selected = []
        for element in self.elements[book_component]:
            result = selector(element, **kwargs)
            if result:
                selected += [element]
        return selected

    def remove_components(self, book_component, element):
        assert isinstance(element, Element)
        components_table = self.elements[book_component]

        for i in range(0, len(components_table)):
            if (components_table[i])._elem_self == element:
                self._elem_self.remove(element)
                del components_table[i]
                break

    def add_transaction(self, trn):
        assert isinstance(trn, Transaction)
        self._elem_self.append(trn._elem_self)

        trn_elements = self.elements['transactions']
        assert isinstance(trn_elements, list)
        trn_elements += [trn]
