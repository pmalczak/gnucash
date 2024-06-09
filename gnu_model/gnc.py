#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gnu_model import primitive_simple as simple
from gnu_model.book import Book
from gnu_model.xml_element import XmlElement, extract_name_space

__author__ = 'Piotr.Malczak@gpm-sys.com'


class GncV2(XmlElement):
    def __init__(self, elem_self, elements_tree, **kwargs):
        self._xml_attr = ('count-data', 'book')
        self.elements_tree = elements_tree

        super().create_attr(self._xml_attr)
        assert elem_self.tag == 'gnc-v2'
        super().__init__(elem_self, None, None, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'count-data':
                var = simple.CountData(elem, None, None, **kwargs)
            elif tag == 'book':
                var = Book(elem, None, None, **kwargs)
            else:
                raise NotImplementedError

            self.set(tag, var)
        return
