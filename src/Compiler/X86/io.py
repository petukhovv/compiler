# -*- coding: utf-8 -*-

from pprint import pprint

from Utils.write import Write
from Utils.read import Read

def read_statement(compiler):
    Read(compiler).call()

def write_statement(compiler, aexp):
    aexp.compile_x86(compiler)
    Write(compiler).call()
