# -*- coding: utf-8 -*-

from ...Core.registers import Registers
from ...Core.commands import Commands
from ...Core.config import FUNCTIONS_LABEL_PREFIX
from ...Runtime.gc import GC


def call_statement(compiler, node):
    """ Компиляция выражения вызова функции """
    for arg in node.args.elements:
        arg.compile_asm(compiler)
        compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
        GC(compiler).increment()

    function_number = compiler.environment.get_number(node.name)
    compiler.code.add(Commands.CALL, FUNCTIONS_LABEL_PREFIX + str(function_number))

    compiler.code.add(Commands.PUSH, Registers.EAX)
    compile_time_type = compiler.environment.get_return_type(node.name)

    return compiler.types.set(compile_time_type)
