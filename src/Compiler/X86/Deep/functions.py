# -*- coding: utf-8 -*-

from ..Helpers.types import *


class FunctionCompiler:
    @staticmethod
    def args_write(compiler, args):
        # Для всех аргументов создаем переменные
        # И компилируем конструкции изъятия из стека (в обратном порядке) аргументов функции и записи их в environment
        for arg in args.elements:
            compiler.bss.vars.add(arg, 'resb', 255, type=Types.DYNAMIC)
            # type_variable = compiler.bss.vars.add(None, 'resb', 255, type=Types.INT)
            # compiler.code.add('pop', [compiler.bss.vars.get(type_variable)])
            compiler.code.add('pop', [compiler.bss.vars.get(arg)])
            # compiler.code.add('pop', [compiler.bss.vars.get_type(arg)])
