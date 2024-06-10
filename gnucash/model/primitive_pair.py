# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
from gnucash.model import primitive_simple as simple
from gnucash.model.xml_element import XmlElement, extract_name_space


class AccountSlot(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('key', 'value')
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def __str__(self):
        result = '{}:{}'.format(getattr(self, 'key'), getattr(self, 'value'))
        return result

    def retrieve(self, **kwarg):
        i = 0
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'key':
                var = simple.AccountKey(elem, None, None, **kwarg)
                i += 1
            elif tag == 'value':
                var = AccountSlotValue(elem, None, None, **kwarg)
                i += 3
            else:
                raise NotImplementedError
            self.set(tag, var)
        assert i == 4

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, 'slot')
        elem.tail = '\n '
        elem.text = '\n  '

        self.key   = simple.AccountKey(None, elem, args['key'], **kwargs)
        if 'gdate-value' in args:
            self.value = GDateValue(None, elem, args['gdate-value'], **kwargs)
        elif 'string' in args:
            self.value = StringValue(None, elem, args['string'], **kwargs)
        else:
            raise NotImplementedError
        return elem


class TransactionSlot(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('key', 'value')
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwarg):
        i = 0
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'key':
                var = simple.TransactonKey(elem, None, None, **kwarg)
                i += 1
            elif tag == 'value':
                var = GDateValue(elem, None, None, **kwarg)
                i += 3
            else:
                raise NotImplementedError
            self.set(tag, var)
        assert i == 4

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, 'slot')
        elem.tail = '\n '
        elem.text = '\n  '

        self.key   = simple.TransactonKey(None, elem, args['key'], **kwargs)
        if 'gdate-value' in args:
            self.value = GDateValue(None, elem, args['gdate-value'], **kwargs)
        else:
            raise NotImplementedError
        return elem


class GDateValue(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('gdate',)
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwarg):
        i = 0
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'gdate':
                var = simple.GDate(elem, None, None, **kwarg)
            else:
                raise NotImplementedError
            self.set(tag, var)
            i += 1
        assert i in (0, 1)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/slot}value', attrib={'type':'gdate'})
        elem.tail = '\n    '
        elem.text = '\n '

        self.gdate = simple.GDate(None, elem, args['gdate'], **kwargs)
        return elem


class StringValue(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ()
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwarg):
        i = 0
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'gdate':
                var = simple.GDate(elem, None, None, **kwarg)
            else:
                raise NotImplementedError
            self.set(tag, var)
            i += 1
        assert i in (0, 1)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/slot}value', attrib={'type':'string'})
        elem.tail = '\n    '
        elem.text = args
        return elem


class AccountSlotValue(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('slot',)
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwarg):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'slot':
                var = AccountSlot(elem, None, None, **kwarg)
            else:
                raise NotImplementedError
            self.set(tag, var)
