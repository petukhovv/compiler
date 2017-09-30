# -*- coding: utf-8 -*-

from Utils.itoa import Itoa

def write_statement(compiler, aexp):
    aexp.compile_x86(compiler)

    itoa = Itoa(compiler)
    itoa.call()
