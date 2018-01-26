# -*- coding: utf-8 -*-

from .compiler import Compiler


def compile_asm(ast):
    """ Запуск компилятора в код языка ассемблера NASM (x86) """
    compiler = Compiler()

    ast.compile_asm(compiler)

    return compiler.get_result()
