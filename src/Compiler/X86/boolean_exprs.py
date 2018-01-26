from .Helpers.types import *
from .Utils.labels import *
from .Helpers.commands import Commands

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
    left.compile_x86(compiler)
    compiler.commands.clean_type()
    right.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add(Commands.POP, ['ebx'])
    compiler.code.add(Commands.POP, ['eax'])

    compiler.code.add(Commands.CMP, ['ebx', 'eax'])

    true_result_label = TrueResult(compiler)

    compiler.code.add(Commands.MOV, ['eax', 0])
    compiler.code.add(relop_compare_map[op], [true_result_label.get()])
    true_result_label.add_return()
    compiler.code.add(Commands.PUSH, ['eax'])

    return compiler.commands.set_and_return_type(Types.INT)


def and_bexp(compiler, left, right):
    """ 'AND' operator compilation """
    finish_label = compiler.labels.create()
    finish_false_label = compiler.labels.create()

    left.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add(Commands.POP, ['eax'])

    # If the first operand is 0, the second operand is not checked,
    # but immediately go to the false result label (lazy check)
    compiler.code.add(Commands.CMP, ['eax', 1])
    compiler.code.add(Commands.JNZ, [finish_false_label])

    # Otherwise, we will check the second operand
    right.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add(Commands.POP, ['eax'])

    # If the second operand is 0, then go to the false result label
    compiler.code.add(Commands.CMP, ['eax', 1])
    compiler.code.add(Commands.JNZ, [finish_false_label])

    # If both operands are 1, then the result of 'AND' execution is 1, it write to the eax register
    # and go to the completion label 'AND' (bypassing the false result section).
    compiler.code.add(Commands.MOV, ['eax', 1])
    compiler.code.add(Commands.JMP, [finish_label])

    # Section of false result, 0 write to the eax register
    compiler.code.add(finish_false_label + ':', [])
    compiler.code.add(Commands.MOV, ['eax', 0])

    # Complete execution 'AND'
    compiler.code.add(finish_label + ':', [])

    compiler.code.add(Commands.PUSH, ['eax'])

    return compiler.commands.set_and_return_type(Types.BOOL)
