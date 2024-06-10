# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@fingo.net'

import os
from pathlib import Path
from xml.sax import parse

from gnucash.file.gnu2xml_worker import GnuZip2XmlWorker
from gnucash.file.xml_extractor import MyHandler


class GnuAccountsSolverGeneric:
    def __init__(self, gnucash_file: Path = None, xml_file_name: Path = None):
        assert bool(gnucash_file) != bool(xml_file_name)  # logical xor

        self.file_name = gnucash_file if gnucash_file else \
            (str(xml_file_name) if xml_file_name else '')

        self.xml_handler = MyHandler()
        self.accs_by_id = None
        self.accs_by_name_parent = None
        self.guid_name = None

        self._init(gnucash_file, xml_file_name)

        self.accs_by_id = self.xml_handler.accounts
        self.accs_by_name_parent = self._make_dict_by_name_parent()
        self.guid_name = self._make_dict_guid_name()
        return

    def _init(self, _gnu_file_name: Path, xml_file_name: Path):
        # self.xml_handler = MyHandler()

        if _gnu_file_name:
            if not os.path.isfile(_gnu_file_name):
                raise FileExistsError(_gnu_file_name)

            gnu_zip_worker = GnuZip2XmlWorker(_gnu_file_name)
            xml_file_name = ''
            try:
                xml_file_name = gnu_zip_worker.extract()
                parse(xml_file_name, self.xml_handler)
            finally:
                if os.path.isfile(xml_file_name):
                    os.remove(xml_file_name)

        else:
            parse(str(xml_file_name), self.xml_handler)

    def _make_dict_by_name_parent(self):
        result = {}
        for account_id, account in self.xml_handler.accounts.items():
            if hasattr(account, 'parent'):
                key = (account.name, account.parent)
                assert key not in result
                result[key] = account
        return result

    def __make_dict_guid_name(self, _result, table):
        assert isinstance(_result, dict)
        assert isinstance(table, list)

        result_table = table
        while len(result_table) > 0:
            elem = result_table[0]
            result_table = result_table[1:]
            if hasattr(elem, 'parent'):
                if elem.parent in _result:
                    _parent = _result[elem.parent]
                    _name = _parent['name'] + ':' if _parent['name'] else ''
                    _r = {'name':  _name + elem.name,
                          'parent': elem.parent
                          }
                    _id = elem.id
                    _result[_id] = _r
                else:
                    result_table = self.__make_dict_guid_name(_result, result_table)
            else:
                _r = {'name': '',
                      'parent': None
                      }
                _id = elem.id
                _result[_id] = _r

        return result_table

    def _accs_by_id_as_table(self) -> list:
        result = []
        for key, item in self.accs_by_id.items():
            result += [item]
        return result

    def _make_dict_guid_name(self) -> dict:
        assert self.accs_by_name_parent is not None
        result = {}

        table = self._accs_by_id_as_table()
        self.__make_dict_guid_name(result, table)
        result = self._reduce(result)

        return result

    @staticmethod
    def _reduce(dict_by_id):
        assert isinstance(dict_by_id, dict)
        result = {}
        for k, v in dict_by_id.items():
            result[k] = v['name']
        return result

    # def _reverse(self, dict_by_id):
    #     assert isinstance(dict_by_id, dict)
    #     result = {}
    #     for k, v in dict_by_id.items():
    #         _r = {'id': k,
    #               'parent': v['parent']}
    #         result[v['name']] = _r
    #     return result

    def _find_root_id(self):
        for acc_id, acc in self.xml_handler.accounts.items():
            if acc.name == "Root Account":
                return acc.id
        raise IndexError
