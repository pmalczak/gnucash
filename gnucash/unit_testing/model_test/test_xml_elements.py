# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import unittest
from xml.etree.ElementTree import Element, tostring


class XmlElementsTester(unittest.TestCase):

    def test_simple_elements(self):
        a = Element('a')
        a.text = '----a-----'
        b = Element('b')
        b.append(a)
        result = tostring(b)
        expected = b'<b><a>----a-----</a></b>'
        self.assertTrue(result == expected)


if __name__ == '__main__':

    unittest.main()
