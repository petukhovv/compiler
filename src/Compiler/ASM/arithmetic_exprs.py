from .Helpers.types import *
from .Helpers.commands import Commands
from .Helpers.registers import Registers

""" Map: arithmetic operator in programming language = arithmetic operator in ASM """
binop_compare_map = {
    '+': {
        'operator': Commands.ADD,
        'operands': [Registers.EAX, Registers.EBX]
    },
    '-': {
        'operator': Commands.SUB,
        'operands': [Registers.EAX, Registers.EBX]
    },
    '*': {
        'operator': Commands.MUL,
        'operands': [Registers.EBX]
    },
    '/': {
        'operator': Commands.IDIV,
        'operands': [Registers.EBX]
    },
    '%': {
        'operator': Commands.DIV,
        'operands': [Registers.EBX]
    }
}


def int_aexp(compiler, i):
    """ Integer compilation """
    compiler.code.add(Commands.MOV, [Registers.EAX, i])
    compiler.code.add(Commands.PUSH, [Registers.EAX])

    return compiler.commands.set_and_return_type(Types.INT)


def binop_aexp(compiler, op, left, right):
    """ Arithmetic expression compilation """
    left.compile_asm(compiler)
    compiler.commands.clean_type()
    right.compile_asm(compiler)
    compiler.commands.clean_type()
    compiler.code.add(Commands.POP, [Registers.EBX])
    compiler.code.add(Commands.POP, [Registers.EAX])

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])

    if op == '%':
        compiler.code.add(Commands.MOVZX, [Registers.EAX, Registers.DX])

    compiler.code.add(Commands.PUSH, [Registers.EAX])

    return compiler.commands.set_and_return_type(Types.INT)


def var_aexp(compiler, name, context, value_type):
    """ Variable compilation """
    if context == 'assign':
        compiler.bss.vars.add(name, 'resb', 4, value_type)
        compiler.code.add(Commands.POP, [compiler.bss.vars.get(name)])
    else:
        compiler.code.add(Commands.MOV, [Registers.EAX, compiler.bss.vars.get(name)])
        compiler.code.add(Commands.PUSH, [Registers.EAX])
        compile_time_type = compiler.bss.vars.get_compile_time_type(name)

        return compiler.commands.set_and_return_type(compile_time_type)
