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

    compiler.code.add(Commands.POP, Registers.EBX)\
        .add(Commands.POP, Registers.EAX)\
        .add(Commands.CMP, [Registers.EBX, Registers.EAX])\
        .add(Commands.MOV, [Registers.EAX, 0])\
        .add(relop_compare_map[op], true_result_label)

    compiler.code.add(Commands.MOV, [Registers.EAX, 0])\
        .add(Commands.JMP, finish_label)

    compiler.code.add_label(true_result_label)\
        .add(Commands.MOV, [Registers.EAX, 1])

    compiler.code.add_label(finish_label)\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def and_bexp(compiler, left, right):
    """ 'AND' operator compilation """
    finish_label = compiler.labels.create()
    false_result_label = compiler.labels.create()

    left.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EAX)

    # If the first operand is 0, the second operand is not checked,
    # but immediately go to the false result label (lazy check)
    compiler.code.add(Commands.CMP, [Registers.EAX, 0])\
        .add(Commands.JZ, false_result_label)

    # Otherwise, we will check the second operand
    right.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EAX)

    # If the second operand is 0, then go to the false result label
    compiler.code.add(Commands.CMP, [Registers.EAX, 0])\
        .add(Commands.JZ, false_result_label)

    # If both operands are 1, then the result of 'AND' execution is 1, it write to the eax register
    # and go to the completion label 'AND' (bypassing the false result section).
    compiler.code.add(Commands.MOV, [Registers.EAX, 1])\
        .add(Commands.JMP, finish_label)

    # Section of false result, 0 write to the eax register
    compiler.code.add_label(false_result_label)\
        .add(Commands.MOV, [Registers.EAX, 0])

    # Complete execution 'AND'
    compiler.code.add_label(finish_label)\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.BOOL)


def or_bexp(compiler, left, right):
    """ 'OR' operator compilation """
    finish_label = compiler.labels.create()
    finish_true_label = compiler.labels.create()

    left.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EAX)

    # If the first operand is not equal 0, the second is not checked,
    # but immediately go to the true result label (lazy check)
    compiler.code.add(Commands.CMP, [Registers.EAX, 0])\
        .add(Commands.JNZ, finish_true_label)

    # Otherwise, we will check the second operand
    right.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EAX)

    # If the second operand is not equal 0, then go to the true result label
    compiler.code.add(Commands.CMP, [Registers.EAX, 0])\
        .add(Commands.JZ, finish_true_label)

    # If both operands are 0, then the result of 'OR' execution is 0, it write to the eax register
    # and go to the completion label 'OR' (bypassing the true result section).
    compiler.code.add(Commands.MOV, [Registers.EAX, 0])\
        .add(Commands.JMP, finish_label)

    # Section of true result, 1 write to the eax register
    compiler.code.add_label(finish_true_label)\
        .add(Commands.MOV, [Registers.EAX, 1])

    # Complete execution 'OR'
    compiler.code.add_label(finish_label)\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.BOOL)


def not_bexp(compiler, exp):
    """ 'NOT' operator compilation """
    finish_label = compiler.labels.create()
    false_result_label = compiler.labels.create()
    
    exp.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EAX)

    # If the operand is equal 0, go to the false result section
    compiler.code.add(Commands.CMP, [Registers.EAX, 0])\
        .add(Commands.JZ, false_result_label)

    # Section of true result, 1 write to the eax register
    compiler.code.add(Commands.MOV, [Registers.EAX, 1])\
        .add(Commands.JMP, finish_label)

    # Section of true result, 0 write to the eax register
    compiler.code.add_label(false_result_label)\
        .add(Commands.MOV, [Registers.EAX, 0])

    # Complete execution 'NOT'
    compiler.code.add_label(finish_label)\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.BOOL)
