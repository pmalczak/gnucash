# -*- coding: utf-8 -*-

from gnucash.model import primitive_simple as simple, primitive_tuple as tuple_elem
from gnucash.model.primitive_composite import Currency, DatePosted, DateEntered
from gnucash.model.xml_element import XmlElement, extract_name_space

__author__ = 'Piotr.Malczak@gpm-sys.com'


class Transaction(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('id', 'currency', 'num', 'date-posted', 'date-entered', 'description', 'splits', 'slots')

        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'id':
                var = simple.TrnId(elem, None, None, **kwargs)
            elif tag == 'currency':
                var = Currency(elem, None, None, **kwargs)
            elif tag == 'num':
                var = simple.Num(elem, None, None, **kwargs)
            elif tag == 'date-posted':
                var = DatePosted(elem, None, None, **kwargs)
            elif tag == 'date-entered':
                var = DateEntered(elem, None, None, **kwargs)
            elif tag == 'description':
                var = simple.TransactionDescription(elem, None, None, **kwargs)
            elif tag == 'slots':
                var = tuple_elem.TransactionSlots(elem, None, None, **kwargs)
            elif tag == 'splits':
                var = tuple_elem.Splits(elem, None, None, **kwargs)
            else:
                raise NotImplementedError

            self.set(tag, var)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/gnc}transaction', attrib={'version':'2.0.0'})
        elem.tail = '\n'
        elem.text = '\n  '

        setattr(self, 'id',  simple.TrnId(None, elem, args['id'], **kwargs))
        self.currency    = Currency(None, elem, args['currency'], **kwargs)
        if args['num']:
            self.num     = simple.Num(None, elem, args['num'], **kwargs)
        setattr(self, 'date-posted',  DatePosted(None, elem, args['date-posted'], **kwargs))
        setattr(self, 'date-entered', DateEntered(None, elem, args['date-entered'], **kwargs))
        self.description = simple.TransactionDescription(None, elem, args['description'], **kwargs)
        self.slots       = tuple_elem.TransactionSlots(None, elem, args['slots'], **kwargs)
        self.splits      = tuple_elem.Splits(None, elem, args['splits'], **kwargs)
        return elem
