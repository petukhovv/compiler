from .Core.types import *
from .Runtime.read import Read
from .Runtime.write import Write


def read_statement(compiler, node):
    Read(compiler).call()
    return compiler.types.set(Types.INT)


def write_statement(compiler, node):
    value_type = node.aexp.compile_asm(compiler)
    compiler.types.pop()
    Write(compiler).call(value_type)
