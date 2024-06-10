# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@fingo.net'

from pathlib import Path


class CouldNotObtainLock(Exception):
    pass


class GnuFileLocks:
    def __init__(self, gnu_file: Path):
        assert isinstance(gnu_file, Path)
        gnu_file = gnu_file.absolute()

        if not gnu_file.is_file():
            raise FileExistsError(str(gnu_file))

        self.gnu_file = gnu_file

    def is_locked(self):
        lck_file = self._lock_file_name()
        return lck_file.is_file()

    def obtain_lock(self) -> None:
        if self.is_locked():
            raise CouldNotObtainLock
        with open(self._lock_file_name(), mode='w') as f:
            pass

    def release_lock(self):
        lck_file = self.__lock_file_name__()
        lck_file.unlink()

    def _release_lock(self):
        lck_file = self._lock_file_name()
        lck_file.unlink()

    def __lock_file_name__(self) -> Path:
        f = self.gnu_file.absolute()
        lck_file = f.parent / f'{f.name}.LCK'
        return lck_file

    def _lock_file_name(self):
        if not self.gnu_file.is_file():
            raise FileExistsError
        return self.__lock_file_name__()
