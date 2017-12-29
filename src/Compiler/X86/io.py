# -*- coding: utf-8 -*-

from pprint import pprint

from .Helpers.types import *
from .Utils.write import Write
from .Utils.read import Read


def read_statement(compiler):
    Read(compiler).call()

    return Types.INT


def write_statement(compiler, aexp):
    value_type = aexp.compile_x86(compiler)
    Write(compiler).call(value_type)
