# -*- coding: utf-8 -*-

from ...Deep.strings import StringCompiler


def strset(compiler, node):
    """ Компиляция built-in функции strset (задание символа строки) """
    node.args.elements[2].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strset(compiler)
