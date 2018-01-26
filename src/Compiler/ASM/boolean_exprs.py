from .Core.types import *
from .Core.commands import Commands
from .Core.registers import Registers

""" Map: logic operator in programming language = the corresponding jump instruction in ASM """
relop_compare_map = {
    '==':   Commands.JE,
    '!=':   Commands.JNE,
    '<':    Commands.JG,
    '<=':   Commands.JGE,
    '>':    Commands.JL,
    '>=':   Commands.JLE
}


def relop_bexp(compiler, op, left, right):
    """ Logic expression compilation """
    finish_label = compiler.labels.create()
    true_result_label = compiler.labels.create()

    left.compile_asm(compiler)
    compiler.types.pop()
    right.compile_asm(compiler)
    compiler.types.pop()

    compiler.code.add(Commands.POP, [Registers.EBX])
    compiler.code.add(Commands.POP, [Registers.EAX])
    compiler.code.add(Commands.CMP, [Registers.EBX, Registers.EAX])
    compiler.code.add(Commands.MOV, [Registers.EAX, 0])
    compiler.code.add(relop_compare_map[op], [true_result_label])

    compiler.code.add(Commands.MOV, [Registers.EAX, 0])
    compiler.code.add(Commands.JMP, [finish_label])

    compiler.code.add(true_result_label + ':', [])
    compiler.code.add(Commands.MOV, [Registers.EAX, 1])

    compiler.code.add(finish_label + ':', [])
    compiler.code.add(Commands.PUSH, [Registers.EAX])

    return compiler.types.set(Types.INT)


def and_bexp(compiler, left, right):
    """ 'AND' operator compilation """
    finish_label = compiler.labels.create()
    false_result_label = compiler.labels.create()

    left.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, [Registers.EAX])

    # If the first operand is 0, the second operand is not checked,
    # but immediately go to the false result label (lazy check)
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])
    compiler.code.add(Commands.JNZ, [false_result_label])

    # Otherwise, we will check the second operand
    right.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, [Registers.EAX])

    # If the second operand is 0, then go to the false result label
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])
    compiler.code.add(Commands.JNZ, [false_result_label])

    # If both operands are 1, then the result of 'AND' execution is 1, it write to the eax register
    # and go to the completion label 'AND' (bypassing the false result section).
    compiler.code.add(Commands.MOV, [Registers.EAX, 1])
    compiler.code.add(Commands.JMP, [finish_label])

    # Section of false result, 0 write to the eax register
    compiler.code.add(false_result_label + ':', [])
    compiler.code.add(Commands.MOV, [Registers.EAX, 0])

    # Complete execution 'AND'
    compiler.code.add(finish_label + ':', [])

    compiler.code.add(Commands.PUSH, [Registers.EAX])

    return compiler.types.set(Types.BOOL)
