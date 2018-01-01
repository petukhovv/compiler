# -*- coding: utf-8 -*-

from ..Helpers.types import *


class FunctionCompiler:
    @staticmethod
    def args_write(compiler, args):
        # Для всех аргументов создаем переменные
        # И компилируем конструкции изъятия из стека (в обратном порядке) аргументов функции и записи их в environment
        args_map = {k: v for v, k in enumerate(args.elements)}
        compiler.environment.set_args(args_map)
