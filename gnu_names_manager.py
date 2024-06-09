# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import datetime
from pathlib import Path


def date_based_file_name(gnu_file: Path, **kwargs) -> Path:
    _t_ = {
        'SALE': 'SALE-%Y%m%d-%H%M.gnucash'
    }
    gnu_file = gnu_file.absolute()

    _core = gnu_file.name.split('.')[0]
    _begining = _core[0:4]

    _t = _t_[_begining]
    _core_new = datetime.datetime.now().strftime(_t)
    result = gnu_file.parent / _core_new
    return result


def template_based_file_name(gnu_file: Path, new_core_name='SALE', **kwargs) -> Path:
    _ext = '_new'
    gnu_file = gnu_file.absolute()
    _core = gnu_file.name.split('.')[0]
    _new_core = _core.replace('GPM', new_core_name)
    gnucash_file_out = gnu_file.parent / f'{_new_core}{_ext}.gnucash'
    return gnucash_file_out
