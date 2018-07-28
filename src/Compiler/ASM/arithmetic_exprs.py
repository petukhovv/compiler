from .Core.registers import Registers
from .Core.types import *
from .Runtime.gc import GC

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
        'operator': Commands.IDIV,
        'operands': [Registers.EBX]
    }
}


def int_aexp(compiler, i):
    """ Integer compilation """
    compiler.code.add(Commands.MOV, [Registers.EAX, i])\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def binop_aexp(compiler, op, left, right):
    """ Arithmetic expression compilation """
    left.compile_asm(compiler)
    compiler.types.pop()
    right.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EBX)\
        .add(Commands.POP, Registers.EAX)

    if op == '/' or op == '%':
        compiler.code.add(Commands.CDQ)

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])

    if op == '%':
        compiler.code.add(Commands.MOV, [Registers.EAX, Registers.EDX])

    compiler.code.add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def var_aexp(compiler, name, context, value_type):
    """ Variable compilation """
    if context == 'assign':
        gc = GC(compiler)

        if compiler.environment.is_exist_local_var(name):
            var = compiler.environment.get_local_var(name)
            var_type = compiler.environment.get_local_var_runtime_type(name)
            compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % Registers.ESP])
            compiler.code.add(Commands.MOV, [var_type, Registers.EAX])
            compiler.environment.update_local_var_type(name, value_type)

            compiler.code.add(Commands.MOV, [Registers.EAX, var])
            compiler.code.add(Commands.MOV, [Registers.EBX, var_type])
            gc.decrement()
        else:
            var = compiler.environment.add_local_var(value_type, name)
            var_type = compiler.environment.get_local_var_runtime_type(name)

        if compiler.environment.defined_object is not None:
            compiler.environment.set_link_object(var, compiler.environment.defined_object)
            compiler.environment.defined_object = None

        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
        compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
        gc.increment()

        compiler.code.add(Commands.POP, var_type)
        compiler.code.add(Commands.POP, var)
    else:
        compiler.code.add(Commands.MOV, [Registers.EAX, compiler.environment.get_local_var(name)])\
            .add(Commands.PUSH, Registers.EAX)
        runtime_var_type = compiler.environment.get_local_var_runtime_type(name)
        compiler.types.set(runtime_var_type)

        var_type = compiler.environment.get_local_var_type(name)
        return var_type
