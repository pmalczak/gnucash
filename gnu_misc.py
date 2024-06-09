# -*- coding: utf-8 -*-
__author__ = 'Piotr'
import os


def get_core_name(gnu_cash_file_name) -> str:
    file_name = os.path.basename(gnu_cash_file_name)
    return os.path.splitext(file_name)[0]
