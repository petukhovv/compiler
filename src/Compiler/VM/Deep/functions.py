# -*- coding: utf-8 -*-

from src.VM.types import *

from ..Helpers.base import *

class FunctionCompiler:
    @staticmethod
    def args_write(commands, data, args):
        # Для всех аргументов создаем переменные
        arg_names = []
        for arg in args.elements:
            arg_names.append(data.var(alias=arg, type=types.DYNAMIC, double_size=True))

        # Компилируем конструкции изъятия из стека (в обратном порядке) аргументов функции и записи их в environment
        for _ in args.elements:
            type_variable = data.var(type=types.INT)
            commands.add(Store, type_variable)
            commands.store_value(arg_names.pop(), type_variable=type_variable)