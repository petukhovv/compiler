# -*- coding: utf-8 -*-

from ...Deep.functions import FunctionCompiler

from ...Helpers.commands import Jump, Return, Label, Function


def function(commands, data, node):
    """ Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
    start_function = data.start_function(node.name)
    finish_function = data.label()

    # При последовательном выполнении пропускаем выполнение тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже
    commands.add(Jump, finish_function)

    # На эту метку переходим при вызове
    commands.add(Function, start_function)

    FunctionCompiler.args_write(commands, data, node.args)

    # Компилируем код тела функции
    node.body.compile_vm(commands, data)

    # Компилируем конструкцию возврата к месту вызова
    commands.add(Return)\
        .add(Label, finish_function)

    data.finish_function()
