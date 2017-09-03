# -*- coding: utf-8 -*-

""" Хелпер для компиляции заданных аргументов built-in функций """
def args_compile(args, numbers, commands, env):
    if isinstance(numbers, list):
        for number in numbers:
            args.elements[number].compile_vm(commands, env)
    else:
        args.elements[numbers].compile_vm(commands, env)
