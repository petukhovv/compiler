from .Helpers.types import *
from .Helpers.commands import Commands

""" Map: arithmetic operator in programming language = arithmetic operator in ASM """
binop_compare_map = {
    '+': {
        'operator': Commands.ADD,
        'operands': ['eax', 'ebx']
    },
    '-': {
        'operator': Commands.SUB,
        'operands': ['eax', 'ebx']
    },
    '*': {
        'operator': Commands.MUL,
        'operands': ['ebx']
    },
    '/': {
        'operator': Commands.IDIV,
        'operands': ['ebx']
    },
    '%': {
        'operator': Commands.DIV,
        'operands': ['ebx']
    }
}


def int_aexp(compiler, i):
    """ Integer compilation """
    compiler.code.add(Commands.MOV, ['eax', i])
    compiler.code.add(Commands.PUSH, ['eax'])

    return compiler.commands.set_and_return_type(Types.INT)


def binop_aexp(compiler, op, left, right):
    """ Arithmetic expression compilation """
    left.compile_x86(compiler)
    compiler.commands.clean_type()
    right.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add(Commands.POP, ['ebx'])
    compiler.code.add(Commands.POP, ['eax'])

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])

    if op == '%':
        compiler.code.add(Commands.MOVZX, ['eax', 'dx'])

    compiler.code.add(Commands.PUSH, ['eax'])

    return compiler.commands.set_and_return_type(Types.INT)


def var_aexp(compiler, name, context, value_type):
    """ Variable compilation """
    if context == 'assign':
        compiler.bss.vars.add(name, 'resb', 4, value_type)
        compiler.code.add(Commands.POP, [compiler.bss.vars.get(name)])
    else:
        compiler.code.add(Commands.MOV, ['eax', compiler.bss.vars.get(name)])
        compiler.code.add(Commands.PUSH, ['eax'])
        compile_time_type = compiler.bss.vars.get_compile_time_type(name)

        return compiler.commands.set_and_return_type(compile_time_type)
