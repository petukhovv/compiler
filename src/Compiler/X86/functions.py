# -*- coding: utf-8 -*-

from .Deep.functions import *


def function(compiler, name, args, body):
    """ Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
    start_function = compiler.environment.start_function(name)
    finish_function = compiler.labels.create()

    # При последовательном выполнении пропускаем выполнение тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже
    compiler.code.add('jmp near', [finish_function])

    # На эту метку переходим при вызове
    compiler.code.add('_fun_' + str(start_function) + ':', [])

    compiler.code.add('push', ['ebp'])
    compiler.code.add('mov', ['ebp', 'esp'])

    # Привязываем мапу аргументов с их порядковыми номерами к метке функции
    args_map = {k: v for v, k in enumerate(args.elements)}
    compiler.environment.set_args(args_map)

    # Компилируем код тела функции
    body.compile_x86(compiler)

    return_type = compiler.environment.get_return_type(name)

    if not return_type:
        compiler.code.add('pop', ['eax'])
        # Компилируем конструкцию возврата к месту вызова
        compiler.code.add('mov', ['esp', 'ebp'])
        compiler.code.add('pop', ['ebp'])
        env = compiler.environment
        args = env.labels[env.current_function]['args']
        compiler.code.add('ret', [len(args) * 4])

    compiler.code.add(finish_function + ':', [])

    compiler.environment.finish_function()


def return_statement(compiler, expr):
    """ Компиляция выражения возврата к месту вызова """
    return_type = expr.compile_x86(compiler)
    compiler.commands.clean_type()

    compiler.code.add('pop', ['eax'])
    # Компилируем конструкцию возврата к месту вызова
    compiler.code.add('mov', ['esp', 'ebp'])
    compiler.code.add('pop', ['ebp'])
    env = compiler.environment
    args = env.labels[env.current_function]['args']
    compiler.environment.set_return_type(return_type)
    compiler.code.add('ret', [len(args) * 4])


def call_statement(compiler, name, args):
    """ Компиляция выражения вызова функции """
    for arg in args.elements:
        arg.compile_x86(compiler)
        compiler.commands.clean_type()

    function_label = compiler.environment.get_label(name)
    compiler.code.add('call', ['_fun_' + str(function_label)])
    compiler.code.add('push', ['eax'])
    compile_time_type = compiler.environment.get_return_type(name)

    return compiler.commands.set_and_return_type(compile_time_type)
