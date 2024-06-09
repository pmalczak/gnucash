# -*- coding: utf-8 -*-
import uuid
__author__ = 'Piotr'


class GUID:
    def __init__(self, value):
        assert isinstance(value, str)
        assert len(value) == 32
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        s = 'GIUD({})'.format(self.value)
        return s

    def __eq__(self, other):
        if isinstance(other, GUID):
            result = self.value == other.value
            return result
        else:
            raise AttributeError

    def __hash__(self):
        result = int(self.value, 16)
        return result


def new_guid():
    guid4 = uuid.uuid4()
    guid = guid4.hex
    return GUID(guid)


def new_guid5(account):
    guid5 = uuid.uuid5(uuid.NAMESPACE_URL, account)
    guid = guid5.hex
    return GUID(guid)


def new_guid5_str(account):
    guid5 = uuid.uuid5(uuid.NAMESPACE_URL, account)
    guid = guid5.hex
    return str(GUID(guid))
