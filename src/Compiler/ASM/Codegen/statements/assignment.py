# -*- coding: utf-8 -*-


def assign_statement(compiler, node):
    """ Компиляция выражения присваивания """
    value_type = node.aexp.compile_asm(compiler)
    node.variable.context = 'assign'
    node.variable.type = value_type
    node.variable.compile_asm(compiler)