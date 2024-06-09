# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@fingo.net'
import os
import time
from pathlib import Path

VENVIRONMENT = 'venv_gnucash'
VENV_INSTALL = 'venv_install.bat'
VENV_UPDATE = 'venv_update.bat'


def main(here: Path):
    home = Path().home()
    # code_dir = Path().home() / CODE_DIR
    # if not code_dir.is_dir():
    #     m = f'Katalog "{code_dir}" nie istnieje'
    #     raise NotADirectoryError(m)

    # if here.parent == code_dir.parent:
    #     if here != code_dir:
    #         m = f'"{code_dir}" to nieprawidłowy katalog startowy'
    #         raise ValueError(m)

    venv = home / VENVIRONMENT
    if not venv.is_dir():
        y = {VENV_INSTALL:
                 (f'call python -m venv %HOMEDRIVE%%HOMEPATH%\\{VENVIRONMENT}\n'
                  f'call %HOMEDRIVE%%HOMEPATH%\\{VENVIRONMENT}\\Scripts\\activate\n'
                  f'call python.exe -m pip install --upgrade pip\n')
             }
        _run_bat_file_(y)

    y = {
        VENV_UPDATE:
            (f'call %HOMEDRIVE%%HOMEPATH%\\{VENVIRONMENT}\\Scripts\\activate\n'
             f'call python.exe -m pip install --upgrade pip\n'
             f'call pip install -r requirements.txt\n')
    }
    _run_bat_file_(y)

    # y ={
    #     here / f'run_APP_2.bat':
    #         (f'call %HOMEDRIVE%%HOMEPATH%\\{VENVIRONMENT}\\Scripts\\activate\n'
    #          f'cd %HOMEDRIVE%%HOMEPATH%\\"{CODE_DIR}"\\dist\n'
    #          f'start python app.py\n'
    #          f'timeout /t 3\n'
    #          f'start msedge http://127.0.0.1:8050/\n')
    # }
    # _run_bat_file_(y)
    return


def _run_bat_file_(arg: dict):
    assert len(arg) == 1
    _file = list(arg.keys())[0]
    _content = arg[_file]

    with open(_file, 'w') as f:
        f.write(_content)

    cmd = f'"{_file}"'
    print(f'CMD: {cmd}')
    os.system(cmd)
    return


if __name__ == '__main__':
    here = os.getcwd()
    try:
        here = Path(here)
        main(here)
    except Exception as e:
        print(str(e))
        time.sleep(5)
    finally:
        os.chdir(here)
