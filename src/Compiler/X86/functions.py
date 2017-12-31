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

    function_call_address_var_name = '_fun_' + str(start_function) + '_call'
    compiler.bss.vars.add(function_call_address_var_name, 'resb', 255)
    compiler.code.add('pop', [compiler.bss.vars.get(function_call_address_var_name)])

    FunctionCompiler.args_write(compiler, args)

    # Компилируем код тела функции
    body.compile_x86(compiler)

    compiler.code.add('push', [compiler.bss.vars.get(function_call_address_var_name)])

    # Компилируем конструкцию возврата к месту вызова
    compiler.code.add('ret', [])

    compiler.code.add(finish_function + ':', [])

    compiler.environment.finish_function()


def return_statement(compiler, expr):
    """ Компиляция выражения возврата к месту вызова """
    return_type = expr.compile_x86(compiler)
    compiler.environment.set_return_type(return_type)


def call_statement(compiler, name, args):
    """ Компиляция выражения вызова функции """
    for arg in args.elements:
        arg.compile_x86(compiler)

    function_label = compiler.environment.get_label(name)
    compiler.code.add('call', ['_fun_' + str(function_label)])

    return compiler.environment.get_return_type(name)
