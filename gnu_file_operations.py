# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import shutil
from pathlib import Path

from .gnu_file_locks import GnuFileLocks
from .gnu_file_operations_primitives import GnuFileOperationsPrimitives
from .gnu_names_manager import date_based_file_name


class GnuFileOperations(GnuFileOperationsPrimitives):

    def tide_up_directory(self) -> None:
        lock = GnuFileLocks(self.gnu_file)
        lock.obtain_lock()
        try:
            self._tide_up_directory()
        finally:
            lock._release_lock()

    def make_new_version_of_gnu_file(self) -> Path:
        assert self.gnu_file.is_file()

        new_gnu_file = date_based_file_name(self.gnu_file)
        backup_dir = self._get_backup_dir_name()
        if GnuFileLocks(self.gnu_file).is_locked():
            raise Exception("occured, so it can't be removed")

        shutil.copyfile(self.gnu_file, new_gnu_file)
        shutil.move(self.gnu_file, backup_dir)
        return new_gnu_file

    def copy_to_backup(self) -> None:
        shutil.copy(self.gnu_file, self._backup_directory)

    def move_to_backup(self) -> None:
        shutil.move(str(self.gnu_file), self._backup_directory)

    def remove_backup_directory_if_empty(self):
        assert self._backup_directory.is_dir()
        content = list(self._backup_directory.glob('*.*'))
        if len(content) == 0:
            shutil.rmtree(self._backup_directory)
