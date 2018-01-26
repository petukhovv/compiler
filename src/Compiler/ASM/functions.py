# -*- coding: utf-8 -*-

from .Core.commands import Commands
from .Core.registers import Registers


def function(compiler, name, args, body):
    """ Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
    start_function = compiler.environment.start_function(name)
    finish_function = compiler.labels.create()

    # При последовательном выполнении пропускаем выполнение тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже
    compiler.code.add(Commands.JMP, [finish_function])

    # На эту метку переходим при вызове
    compiler.code.add('_fun_' + str(start_function) + ':', [])

    compiler.code.add(Commands.PUSH, [Registers.EBP])
    compiler.code.add(Commands.MOV, [Registers.EBP, Registers.ESP])

    # Привязываем мапу аргументов с их порядковыми номерами к метке функции
    args_map = {k: v for v, k in enumerate(args.elements)}
    compiler.environment.set_args(args_map)

    # Компилируем код тела функции
    body.compile_asm(compiler)

    return_type = compiler.environment.get_return_type(name)

    if not return_type:
        # Компилируем конструкцию возврата к месту вызова
        compiler.code.add(Commands.MOV, [Registers.ESP, Registers.EBP])
        compiler.code.add(Commands.POP, [Registers.EBP])
        env = compiler.environment
        args = env.labels[env.current_function]['args']
        compiler.code.add(Commands.RET, [len(args) * 4])

    compiler.code.add(finish_function + ':', [])

    compiler.environment.finish_function()


def return_statement(compiler, expr):
    """ Компиляция выражения возврата к месту вызова """
    return_type = expr.compile_asm(compiler)
    compiler.types.pop()

    compiler.code.add(Commands.POP, [Registers.EAX])
    # Компилируем конструкцию возврата к месту вызова
    compiler.code.add(Commands.MOV, [Registers.ESP, Registers.EBP])
    compiler.code.add(Commands.POP, [Registers.EBP])
    env = compiler.environment
    args = env.labels[env.current_function]['args']
    compiler.environment.set_return_type(return_type)
    compiler.code.add(Commands.RET, [len(args) * 4])


def call_statement(compiler, name, args):
    """ Компиляция выражения вызова функции """
    for arg in args.elements:
        arg.compile_asm(compiler)
        compiler.types.pop()

    function_label = compiler.environment.get_label(name)
    compiler.code.add(Commands.CALL, ['_fun_' + str(function_label)])
    compiler.code.add(Commands.PUSH, [Registers.EAX])
    compile_time_type = compiler.environment.get_return_type(name)

    return compiler.types.set(compile_time_type)
