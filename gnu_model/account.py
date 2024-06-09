#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnu_model import primitive_simple as simple, primitive_tuple as tuple_elem
from gnu_model.primitive_composite import Commodity
from gnu_model.xml_element import XmlElement, extract_name_space

__author__ = 'Piotr.Malczak@gpm-sys.com'


class Account(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('name', 'id', 'type', 'commodity', 'commodity-scu', 'slots', 'parent', 'description')
        self.account_name = None

        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'name':
                var = simple.Name(elem, None, None, **kwargs)
            elif tag == 'id':
                var = simple.ActId(elem, None, None, **kwargs)
                account_name = (kwargs['accounts_name_decoder'])(var.text)
                self.account_name = account_name
            elif tag == 'type':
                var = simple.Type(elem, None, None, **kwargs)
            elif tag == 'commodity':
                var = Commodity(elem, None, None, **kwargs)
            elif tag == 'commodity-scu':
                var = simple.CommodityScu(elem, None, None, **kwargs)
            elif tag == 'slots':
                var = tuple_elem.AccountSlots(elem, None, None, **kwargs)
            elif tag == 'parent':
                var = simple.Parent(elem, None, None, **kwargs)
            elif tag == 'description':
                var = simple.AccountDescription(elem, None, None, **kwargs)

            else:
                raise NotImplementedError
            self.set(tag, var)

    def add_slots(self, slots):
        assert isinstance(slots, tuple_elem.AccountSlots)
        assert self.slots is None

        self._elem_self.append(slots._elem_self)
        self.slots = slots
        return
