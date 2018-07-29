# -*- coding: utf-8 -*-

from ...Core.registers import Registers
from ...Core.commands import Commands
from ...Core.config import FUNCTIONS_LABEL_PREFIX
from ...Core.types import Types

from ...Deep.functions import return_function


def function(compiler, node):
    """ Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
    function_number = compiler.environment.start(node.name)
    finish_function = compiler.labels.create()
    function_start_place = compiler.code.get_current_place() + 4

    # При последовательном выполнении пропускаем выполнение тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже
    compiler.code.add(Commands.JMP, finish_function)

    # На эту метку переходим при вызове
    compiler.code.add_label(FUNCTIONS_LABEL_PREFIX + str(function_number))

    compiler.code.add(Commands.PUSH, Registers.EBP)\
        .add(Commands.MOV, [Registers.EBP, Registers.ESP])

    # Привязываем мапу аргументов с их порядковыми номерами к метке функции
    args_map = {k: v for v, k in enumerate(reversed(node.args.elements))}
    compiler.environment.set_args(args_map)

    # Компилируем код тела функции
    node.body.compile_asm(compiler)

    return_type = compiler.environment.get_return_type(node.name)

    if not return_type:
        compiler.types.set(Types.NOTHING)
        return_function(compiler, args_map)

    compiler.code.add_label(finish_function)

    need_memory = compiler.environment.finish()
    compiler.code.allocate_stack_memory(need_memory, function_start_place)
