# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import datetime
import shutil
from pathlib import Path


def copy_to_backup(gnu_file) -> None:
    shutil.copy(gnu_file, set_backup_dir_name(gnu_file))


def remove_backup_directory_if_empty(gnu_file: Path):
    backup_directory = set_backup_dir_name(gnu_file)
    assert backup_directory.is_dir()
    content = list(backup_directory.glob('*.*'))
    if len(content) == 0:
        shutil.rmtree(backup_directory)


def set_backup_dir_name(gnu_file: Path) -> Path:
    assert gnu_file.is_file()
    result_0 = gnu_file.parent / f'{datetime.datetime.now().year}'
    if not result_0.is_dir():
        result_0.mkdir()

    today = datetime.datetime.now()
    today_str = today.strftime('%Y%m%d-%H%M%S%f')
    result = result_0 / f'{gnu_file.name[:-8]}.{today_str}'
    if not result.is_dir():
        result.mkdir()
    return result
