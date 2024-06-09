# -*- coding: utf-8 -*-
import unittest

from guid import new_guid5

__author__ = 'Piotr.Malczak@gpm-sys.com'


class GuidTestCases(unittest.TestCase):

    def test_uniqueness(self):
        g1 = new_guid5('425')
        g2 = new_guid5('426')
        g3 = new_guid5('425')

        self.assertTrue(g1 == g3)
        self.assertTrue(g1 != g2)

    def test_hashing(self):
        g1 = new_guid5('425').__hash__()
        g2 = new_guid5('426').__hash__()
        g3 = new_guid5('425').__hash__()

        self.assertTrue(g1 == g3)
        self.assertTrue(g1 != g2)


if __name__ == '__main__':

    unittest.main()
