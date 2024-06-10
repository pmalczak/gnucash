# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from gnucash.model import primitive_simple as simple
from gnucash.model.xml_element import XmlElement, extract_name_space


class DatePosted(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('date', )
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'date':
                var = simple.Date(elem, None, None, **kwargs)
            else:
                raise NotImplementedError
            self.set(tag, var)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}date-posted')
        elem.tail = '\n '
        elem.text = '\n  '

        self.date = simple.Date(None, elem, args['date'], **kwargs)
        return elem


class DateEntered(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('date', )
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'date':
                var = simple.Date(elem, None, None, **kwargs)
            else:
                raise NotImplementedError
            self.set(tag, var)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}date-entered')
        elem.tail = '\n '
        elem.text = '\n  '

        self.date = simple.Date(None, elem, args['date'], **kwargs)
        return elem


class ReconcileDate(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('date', )
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'date':
                var = simple.Date(elem, None, None, **kwargs)
            else:
                raise NotImplementedError
            self.set(tag, var)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}date-entered')
        elem.tail = '\n '
        elem.text = '\n  '

        self.date = simple.Date(None, elem, args['date'], **kwargs)
        return elem


class Currency(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('space', 'id')
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'id':
                var = simple.CmdtyId(elem, None, None, **kwargs)
            elif tag == 'space':
                var = simple.Space(elem, None, None, **kwargs)
            else:
                raise NotImplementedError
            self.set(tag, var)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}currency')
        elem.tail = '\n '
        elem.text = '\n  '

        self.space = simple.Space  (None, elem, args['space'], **kwargs)
        self.id    = simple.CmdtyId(None, elem, args['id'], **kwargs)
        return elem


class Split(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('id', 'reconciled-state', 'reconcile-date', 'value', 'quantity', 'account', 'memo', 'action')
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwargs):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'id':
                var = simple.SplitId(elem, None, None, **kwargs)
            elif tag == 'reconciled-state':
                var = simple.ReconciledState(elem, None, None, **kwargs)
            elif tag == 'reconcile-date':
                var = ReconcileDate(elem, None, None, **kwargs)
            elif tag == 'value':
                var = simple.Value(elem, None, None, **kwargs)
            elif tag == 'quantity':
                var = simple.Quantity(elem, None, None, **kwargs)
            elif tag == 'account':
                var = simple.SplitAccount(elem, None, None, **kwargs)
            elif tag == 'memo':
                var = simple.Memo(elem, None, None, **kwargs)
            elif tag == 'action':
                var = simple.Action(elem, None, None, **kwargs)

            else:
                raise NotImplementedError
            self.set(tag, var)

    def init_element(self, constructor, parent, args, **kwargs):
        elem = constructor(parent, '{http://www.gnucash.org/XML/trn}split')
        elem.tail = '\n '
        elem.text = '\n '

        self.id       = simple.SplitId(None, elem, args['id'], **kwargs)
        setattr(self, 'reconciled-state', simple.ReconciledState(None, elem, args['reconciled-state'], **kwargs))
        if 'reconcile-date' in args:
            setattr(self, 'reconcile-date', ReconcileDate(None, elem, args['reconcile-date'], **kwargs))
        self.value    = simple.Value(None, elem, args['value'], **kwargs)
        self.quantity = simple.Quantity(None, elem, args['quantity'], **kwargs)
        self.account  = simple.SplitAccount(None, elem, args['account'], **kwargs)
        if 'memo' in args and args['memo']:
            self.memo = simple.Memo(None, elem, args['memo'], **kwargs)
        if 'action' in args and args['action']:
            self.action = simple.Action(None, elem, args['action'], **kwargs)
        return elem


class Commodity(XmlElement):
    def __init__(self, elem_self, parent, args, **kwargs):
        self._xml_attr = ('space', 'id')
        super().create_attr(self._xml_attr)
        super().__init__(elem_self, parent, args, **kwargs)

    def retrieve(self, **kwarg):
        for elem in self._elem_self:
            name_space, tag = extract_name_space(elem.tag)
            if tag == 'space':
                var = simple.Space(elem, None, None, **kwarg)
            elif tag == 'id':
                var = simple.CmdtyId(elem, None, None, **kwarg)
            else:
                raise NotImplementedError()
            self.set(tag, var)
