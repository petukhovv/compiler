# -*- coding: utf-8 -*-

from .Core.registers import Registers
from .Core.config import FUNCTIONS_LABEL_PREFIX
from .Core.types import *
from .Utils.gc import GC

from .Deep.functions import return_function


def function(compiler, name, args, body):
    """ Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
    function_number = compiler.environment.start(name)
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
    args_map = {k: v for v, k in enumerate(reversed(args.elements))}
    compiler.environment.set_args(args_map)

    # Компилируем код тела функции
    body.compile_asm(compiler)

    return_type = compiler.environment.get_return_type(name)

    if not return_type:
        return_function(compiler, args)

    compiler.code.add_label(finish_function)

    need_memory = compiler.environment.finish()
    compiler.code.allocate_stack_memory(need_memory, function_start_place)


def return_statement(compiler, expr):
    """ Компиляция выражения возврата к месту вызова """
    args = compiler.environment.get_args()
    return_type = expr.compile_asm(compiler)
    compiler.types.pop()
    compiler.environment.set_return_type(return_type)

    if return_type == Types.BOXED_ARR or return_type == Types.UNBOXED_ARR:
        compiler.code.add(Commands.MOV, [Registers.ECX, return_type])
        GC(compiler).increment()

    return_function(compiler, args)


def call_statement(compiler, name, args):
    """ Компиляция выражения вызова функции """
    align_factor = 16
    args_len = len(args.elements)
    stack_remainder = align_factor - ((args_len * 8 + 12) % align_factor)    # +8 - push of return address and saved ebp
    stack_remainder = 0 if stack_remainder == align_factor else stack_remainder
    compiler.code.stack_align(align_factor, stack_remainder)

    for arg in args.elements:
        arg_type = arg.compile_asm(compiler)
        if arg_type == Types.BOXED_ARR or arg_type == Types.UNBOXED_ARR:
            compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
            compiler.code.add(Commands.MOV, [Registers.ECX, arg_type])
            GC(compiler).increment()

    function_number = compiler.environment.get_number(name)
    compiler.code.add(Commands.CALL, FUNCTIONS_LABEL_PREFIX + str(function_number))

    compiler.code.restore_stack_align()

    compiler.code.add(Commands.PUSH, Registers.EAX)
    compile_time_type = compiler.environment.get_return_type(name)

    return compiler.types.set(compile_time_type)
