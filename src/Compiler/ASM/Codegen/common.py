# -*- coding: utf-8 -*-


def enumeration(compiler, node):
    return node.elements


def compound_statement(compiler, node):
    """ Компиляция составного выражения """
    node.first.compile_asm(compiler)
    node.second.compile_asm(compiler)
