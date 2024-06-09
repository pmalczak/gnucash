#!/usr/bin/env python

import re
from xml.etree.cElementTree import dump, SubElement

__author__ = 'Piotr.Malczak@gpm-sys.com'


class XmlElement:
    def __init__(self, elem_self, parent, args, **kwargs):
        if elem_self is not None:
            self._elem_self = elem_self
            self.attrib = elem_self.attrib
            self.text = elem_self.text

            self.retrieve(**kwargs)
        else:
            _elem = self.init_element(SubElement, parent, args, **kwargs)
            self._elem_self = _elem
            self.attrib = _elem.attrib
            self.text = _elem.text

        self.logger = kwargs['logger'] if 'logger' in kwargs else None

    def xml_handler(self):
        return self._elem_self

    def __str__(self):
        return self.text

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            raise NotImplementedError

    def init_element(self, constructor, parent, args, **kwargs):
        raise NotImplementedError

    def create_attr(self, xml_attr):
        for a in xml_attr:
            setattr(self, a, None)

    def log(self, message):
        if self.logger:
            self.logger.log(message)

    def set(self, name, value):
        getattr(self, name)
        setattr(self, name, value)

    def str_attr(self, level):
        try:
            elements = getattr(self, 'elements')
            result = self._str_attr_iter_elements(elements, level)

        except AttributeError:
            result = self._str_attr_iter_attr(level)

        return result

    def _str_attr_iter_elements(self, elements, level):
        result = []
        for elem in elements:
            _res = elem.str_attr(level + 1)
            result += _res

        return result

    def dump(self):
        result = dump(self._elem_self)
        return result

    def _str_attr_iter_attr(self, level):
        result = []
        _format = '{:<17} : {}'
        exlusions = ('status', 'login', 'password', 'connection')

        xml_attr = getattr(self, '_xml_attr')
        for item in xml_attr:
            if item not in exlusions:
                attr = getattr(self, item)
                if attr is not None:
                    if item == 'columnDefDataType':
                        attr = str(attr)
                    elif item == 'query':
                        attr = attr.split('\n')

                    if isinstance(attr, str):
                        res_ = _format.format(item, attr)
                        result += [(level, res_)]
                    elif isinstance(attr, list):
                        _item = item
                        for _attr in attr:
                            res_ = _format.format(_item, _attr)
                            result += [(level, res_)]
                            _item = ''

                    else:
                        res_ = attr.str_attr(level + 1)
                        result += res_

        result += [(level, '')]
        return result


def extract_name_space(text):
    pattern = '^{(.*)}(.*)$'
    result = re.match(pattern, text)
    if result:
        return result.groups()
    else:
        return None, text
