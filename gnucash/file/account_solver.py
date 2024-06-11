# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@fingo.net'

from .account_solver_generic import GnuAccountsSolverGeneric


class AccountDoesNotExist(Exception):
    pass


class GnuAccountsSolver(GnuAccountsSolverGeneric):
    def get_account_name_by_guid(self, guid):
        assert guid in self.guid_name
        result = self.guid_name[guid]
        return result

    def get_guid_by_account(self, account_name):
        splitted_acc = account_name.split(':')
        parent_id = self._find_root_id()

        target_acc = None
        for _id, acc in enumerate(splitted_acc):
            key = (acc, parent_id)
            if key not in self.accs_by_name_parent:
                raise AccountDoesNotExist(account_name)

            target_acc = self.accs_by_name_parent[key]
            parent_id = target_acc.id

        return target_acc.id

    def iban_as_account_name(self, iban: str):
        if iban not in self.iban_mappings:
            raise AccountDoesNotExist(iban)
        result = self.iban_mappings[iban]
        return result
