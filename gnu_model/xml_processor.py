# -*- coding: utf-8 -*-

__author__ = 'Piotr.Malczak@gpm-sys.com'

import os
import gzip
import shutil
import copy
from pathlib import Path

from xml.etree.cElementTree import ElementTree

from gnu_model.transaction import Transaction
from gnu_model.account import Account
from gnu_model.model import GnuObjectModel
from gnu_model.name_spaces import GnuNameSpaces

from gnu_cash.file.account_solver import GnuAccountsSolver
from app_logger.output_console import APP_TEXT_LOGGER


class GnuCashXmlProcessor:
    def __init__(self, gnucash_file: Path):
        assert isinstance(gnucash_file, Path)

        if not gnucash_file.is_file():
            raise FileExistsError

        self.gnu_file = gnucash_file
        self.xml_file = self.xml_file_name(gnucash_file)
        self.gnu_model = None

    def remove_records(self, new_gnucash_file: Path, **kwargs) -> Path:
        assert isinstance(new_gnucash_file, Path)
        self.read_gnu_model()
        removed = self.remove_book_components__2(self.gnu_model, **kwargs)
        if removed:
            self.gnu_model.model2zip(new_gnucash_file)
            APP_TEXT_LOGGER.log(f'nowy {new_gnucash_file}')
            return new_gnucash_file

        else:
            APP_TEXT_LOGGER.log('żadne rekordy nie zostały usunięte')
            return None

    def xml_file_name(self, gnu_file: Path) -> Path:
        assert isinstance(gnu_file, Path)
        _f = gnu_file.absolute()
        xml_file = gnu_file.parent / f'{gnu_file.name[:-8]}.xml'
        return xml_file

    def read_gnu_model(self, delete_xml=True):
        xml_in = self.xml_file_name(self.gnu_file)
        self._gnu2xml(xml_in)
        try:
            tree = self.retrieve_gnu_cash_element_tree(xml_file=xml_in)
            gnu_model = self._get_gnu_object_model(xml_in, tree)
        finally:
            if delete_xml and xml_in.is_file():
                # os.remove(xml_in)
                xml_in.unlink()

        self.gnu_model = gnu_model

    def add_transactions(self, transactions):
        _ext = '_ADD'

        if isinstance(transactions, Transaction):
            self.gnu_model.add_transaction(transactions)
        else:
            raise NotImplementedError

        # _path, __file_in = os.path.split(self.gnu_file)
        # _core, _extension = os.path.splitext(__file_in)
        _core, _extension = tuple(self.gnu_file.name.split('.'))

        # _out_file = _path + '/' + _core + _ext
        gnucash_file_out = self.gnu_file.parent / f'{_core}{_ext}.gnucash'

        # self.gnu_model2zip(gnucash_file_out)
        self.gnu_model.model2zip(gnucash_file_out)

    def amend_accounts(self, select_history_accounts_proc, ammend_acc_proc):
        self.gnu_model.amend_accounts(select_history_accounts_proc, ammend_acc_proc)

    def on_transactions(self, performer, **kwargs):
        self.gnu_model.on_transactions(performer, **kwargs)

    def create_amended_file(self, file_name_procedure, **kwargs):
        gnucash_file_out = file_name_procedure(self.gnu_file, **kwargs)
        assert gnucash_file_out != self.gnu_file
        self.gnu_model.model2zip(gnucash_file_out)
        return gnucash_file_out

    def split_file_name(self, prefix):
        result = self.gnu_file[:-8] + '_' + prefix + '.gnucash'
        return result

    def split(self, split_selector, **kwargs):
        assert self.gnu_model is not None
        result_main = None
        result_splitted = None

        _out_files = {
            'main':     self.split_file_name('main'),
            'splitted': self.split_file_name('splitted'),
        }
        for category, item in _out_files.items():
            if os.path.isfile(item):
                raise FileExistsError

        main_model = copy.deepcopy(self.gnu_model)
        removed_main = self.__remove_book_components__(main_model,
                                                       selector=split_selector, reversed_condition=False, **kwargs)
        if removed_main:
            result_main = GnuCashXmlProcessor(Path(_out_files['main']))
            result_main.gnu_model = main_model
            result_main.gnu_model.gnu_model.model2zip(_out_files['main'])
            self._report_removed(removed_main)

        try:
            splitted_model = copy.deepcopy(self.gnu_model)
            removed_splitted = self.__remove_book_components__(splitted_model,
                                                               selector=split_selector,
                                                               reversed_condition=True, **kwargs)
            if removed_splitted:
                result_splitted = GnuCashXmlProcessor(Path(_out_files['splitted']))
                result_splitted.gnu_model = splitted_model
                result_splitted.gnu_model.model2zip(_out_files['splitted'])
        except Exception:
            _main = _out_files['main']
            if os.path.isfile(_main):
                os.remove(_main)
            raise

        if 'transactions' in split_selector:
            l1_all = len(self.gnu_model.book.elements['transactions'])
            l1_mai = len(result_main.gnu_model.book.elements['transactions']) if result_main else 0
            l1_spl = len(result_splitted.gnu_model.book.elements['transactions']) if result_splitted else 0
            assert l1_all == l1_mai + l1_spl

        if 'assignments' in split_selector:
            l2_all = len(self.gnu_model.book.elements['assignments'])
            l2_mai = len(result_main.gnu_model.book.elements['assignments']) if result_main else 0
            l2_spl = len(result_splitted.gnu_model.book.elements['assignments']) if result_splitted else 0
            assert l2_all == l2_mai + l2_spl

        return {
            'main': result_main,
            'splitted': result_splitted
        }

    def _report_removed(self, removed):
        result = set()
        for item in removed:
            if isinstance(item, Transaction):
                splits = item.splits.elements
                for split in splits:
                    result.add(split.account.account_name)
            elif isinstance(item, Account):
                result.add(item.account_name)
                pass
            else:
                raise NotImplementedError
        with open('removed_accounts.txt', 'wt') as f:
            s = '\n'.join(sorted(list(result)))
            f.write(s)
        return result

    def _get_gnu_object_model(self, xml_in, tree):
        def accounts_name_decoder(guid):
            account_name = account_reader.get_account_name_by_guid(guid)
            return account_name

        account_reader = GnuAccountsSolver(xml_file_name=xml_in)
        gnu_object_model = self._retrieve_object_model_from_elements_tree(tree,
                                                                          accounts_name_decoder=accounts_name_decoder)

        return gnu_object_model

    @staticmethod
    def __remove_book_components__(gnu_model, selector=None, **kwargs):
        removed = []
        assert isinstance(selector, dict)
        for book_component, _selector_function in selector.items():
            _r = gnu_model.remove_book_components(book_component, _selector_function, **kwargs)
            removed += _r
        return removed

    def remove_book_components__2(self, gnu_model, **kwargs):
        return self.__remove_book_components__(gnu_model, **kwargs)

    @staticmethod
    def retrieve_gnu_cash_element_tree(xml_file=None):
        assert xml_file is not None

        GnuNameSpaces()
        tree = ElementTree(file=xml_file)
        return tree

    def _retrieve_object_model_from_elements_tree(self, elements_tree, **kwargs):
        assert isinstance(elements_tree, ElementTree)

        root = elements_tree.getroot()
        if root.tag == 'gnc-v2':
            result = GnuObjectModel(root, elements_tree, **kwargs)
        else:
            raise NotImplementedError
        return result

    def _gnu2xml(self, xml_in):
        with gzip.open(self.gnu_file, 'rt', encoding='utf-8') as f_gnu:
            with open(xml_in, 'wt', encoding='utf-8') as f_xml:
                shutil.copyfileobj(f_gnu, f_xml)
