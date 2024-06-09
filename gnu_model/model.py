# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import gzip
import shutil
from pathlib import Path

from .book import Book
from .gnc import GncV2
from .transaction import Transaction


class GnuObjectModel(GncV2):
    def __init__(self, elem_self, elements_tree, **kwargs):
        super().__init__(elem_self, elements_tree, **kwargs)

    def amend_accounts(self, selector, ammender, **kwargs):
        book = getattr(self, 'book')
        for element in book.elements['assignments']:
            result = selector(element, **kwargs)
            assert isinstance(result, bool)
            if result:
                ammender(element, **kwargs)

    def on_transactions(self, performer, **kwargs):
        book = getattr(self, 'book')
        for element in book.elements['transactions']:
            performer(element, **kwargs)

    def add_transaction(self, trn):
        assert isinstance(trn, Transaction)
        assert isinstance(self.book, Book)
        self.book.add_transaction(trn)

    def remove_book_components(self, book_component, elements_selector, **kwargs):
        selected = self.book.select_components(book_component, elements_selector, **kwargs)
        if selected:
            self.log('Removed transactions:')
            for element in selected:
                self.book.remove_components(book_component, element._elem_self)
        return selected

    def model2zip(self, gnucash_file: Path):
        xml_file = gnucash_file.parent / f'{gnucash_file.name[:-8]}.xml'

        try:
            self.elements_tree.write(xml_file, encoding='UTF-8', xml_declaration='version="1.0" encoding="utf-8" ')
            with open(xml_file, 'rt', encoding='utf-8') as f_in:
                with gzip.open(gnucash_file, 'wt', encoding='utf-8') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        finally:
            if xml_file.is_file():
                xml_file.unlink()
