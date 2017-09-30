# -*- coding: utf-8 -*-

from pprint import pprint

""" Компиляция выражения присваивания """
def assign_statement(compiler, variable, aexp):
    value_type = aexp.compile_x86(compiler)

    variable.context = 'assign'
    variable.type = value_type
    variable.compile_x86(compiler)

def compound_statement(compiler, first, second):
    first.compile_x86(compiler)
    second.compile_x86(compiler)
