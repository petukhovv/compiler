# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop

class FunctionCompiler:
    @staticmethod
    def args_wrtite(commands, env, args):
        # Для всех аргументов создаем переменные
        arg_names = []
        for arg in args.elements:
            arg_names.append(env.var(arg))

        # Компилируем конструкции изъятия из стека (в обратном порядке) аргументов функции и записи их в environment
        for _ in args.elements:
            commands.add(Store, arg_names.pop())
