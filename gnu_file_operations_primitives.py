# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@fingo.net'

import datetime
import glob
import shutil
import time
from pathlib import Path

from .gnu_logs.collect_logs_content import collect_logs_content


class GnuFileOperationsPrimitives:
    def __init__(self, gnu_file: Path):
        assert isinstance(gnu_file, Path)
        gnu_file = gnu_file.absolute()

        if not gnu_file.is_file():
            raise FileExistsError(str(gnu_file))

        self.gnu_file = gnu_file
        self._aggregated_log_file = gnu_file.parent / 'gnu_file.log'
        self._backup_directory = self._set_backup_dir_name()
        self._waste_directory = self._set_waste_dir()

    def _set_backup_dir_name(self) -> Path:
        assert self.gnu_file.is_file()
        result_0 = self.gnu_file.parent / f'{datetime.datetime.now().year}'
        if not result_0.is_dir():
            result_0.mkdir()

        today = datetime.datetime.now()
        today_str = today.strftime('%Y%m%d-%H%M%S%f')
        result = result_0 / f'{self.gnu_file.name[:-8]}.{today_str}'
        if not result.is_dir():
            result.mkdir()
        return result

    def _set_waste_dir(self) -> Path:
        assert self.gnu_file.is_file()
        result_z_del = self.gnu_file.parent / 'z_del'
        if not result_z_del.is_dir():
            result_z_del.mkdir()

        today = datetime.datetime.now()
        today_str = today.strftime('%Y%m%d-%H%M%S%f')
        result = result_z_del / today_str
        if not result.is_dir():
            result.mkdir()
        else:
            today = today + datetime.timedelta(microseconds=1)
            today_str = today.strftime('%Y%m%d-%H%M%S%f')
            result = result_z_del / today_str
            if not result.is_dir():
                result.mkdir()
            else:
                raise NotImplementedError

        return result

    def _tide_up_directory(self) -> None:
        assert self.gnu_file.is_file()

        log_template = str(self.gnu_file.parent / "*.gnucash.*.log")
        gnu_template = str(self.gnu_file.parent / "*.gnucash.*.gnucash")

        backup_dir = self._get_backup_dir_name()
        waste_dir = self._get_gnu_waste_dir()
        aggregated_log_file = self.aggregated_log_file_name()
        collect_logs_content(log_template, aggregated_log_file)

        self._move_files_to_directory(str(aggregated_log_file), backup_dir)
        self._move_files_to_directory(log_template, backup_dir)
        self._move_files_to_directory(gnu_template, waste_dir)

    def _get_backup_dir_name(self) -> Path:
        return self._backup_directory

    def _get_gnu_waste_dir(self) -> Path:
        return self._waste_directory

    def aggregated_log_file_name(self) -> Path:
        return self._aggregated_log_file

    def _move_files_to_directory(self, files_template: str, target_directory: Path):
        assert isinstance(target_directory, Path)
        if not isinstance(files_template, str):
            raise AttributeError(str(files_template))

        if not target_directory.is_dir():
            raise Exception(f"directory {target_directory} doesn't exist")

        files_list = glob.glob(files_template)
        for a_file in files_list:
            self._move_file_to_directory(a_file, target_directory)
        return

    def _move_file_to_directory(self, a_file: str, target_directory: Path):
        if not isinstance(a_file, str):
            raise AttributeError(a_file)
        attempts = 5
        while attempts > 0:
            try:
                shutil.move(a_file, target_directory)
                return

            except PermissionError:
                time.sleep(0.5)
                attempts -= 1

        raise NotImplementedError
