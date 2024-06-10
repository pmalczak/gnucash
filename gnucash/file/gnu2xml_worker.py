#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
import os
from pathlib import Path

__author__ = 'Piotr.Malczak@gpm-sys.com'


class GnuZip2XmlWorker:
    def __init__(self, gnu_file_name: Path):
        self.file_names_processor = FileNamesProcessor(gnu_file_name)

    def extract(self):
        gf = self.file_names_processor.gnu_file_name()
        if not os.path.isfile(gf):
            s = 'file {} not found\n{}'.format(gf, str(self.file_names_processor))
            raise Exception(s)

        with gzip.GzipFile(gf, mode="r") as z:
            ret = z.read()

        xml_file_name = self.file_names_processor.xml_file()
        with open(xml_file_name, "wb") as xml_file:
            xml_file.write(ret)

        return xml_file_name


class FileNamesProcessor:
    def __init__(self, gnu_file: Path):
        if not os.path.isfile(gnu_file):
            raise FileExistsError

        s1 = os.path.split(gnu_file)
        if not s1[0]:
            raise Exception('Provide full path')
        self.working_directory = s1[0] + '/'

        s2 = os.path.splitext(s1[1])
        self._gnu_file = gnu_file
        self._gnu_core = s2[0]

    def __str__(self):
        s = 'gnu: {} working directory {}'.format(self._gnu_file, self.working_directory)
        return s

    def gnu_file_name(self):
        return self._gnu_file

    def xml_file(self):
        core = self._gnu_core
        result = self.working_directory + core + '.xml'
        return result
