#!/usr/bin/env python

__author__ = 'Piotr.Malczak@gpm-sys.com'


class IBAN:
    def __init__(self, value):
        self.var = None
        if isinstance(value, int):
            _var = str(value)
            self.var = _var if len(_var) == 26 else '0' + _var
            assert len(self.var) == 26
        elif isinstance(value, str):
            self.var = value.replace(' ', '')
            assert len(self.var) == 26
        else:
            raise Exception("!")

    def __str__(self):
        return self.var[0:2] + ' ' + \
               self.var[2:6] + ' ' + \
               self.var[6:10] + ' ' + \
               self.var[10:14] + ' ' + \
               self.var[14:18] + ' ' + \
               self.var[18:22] + ' ' + self.var[22:]

    def __eq__(self, other):
        if isinstance(other, str):
            if other[0] == "'":
                _other = other[1:-1]
            else:
                _other = other
            assert len(_other) in (0, 26)
            return self.var == _other
        elif isinstance(other, IBAN):
            return self.var == other.var
        else:
            raise Exception("!")
