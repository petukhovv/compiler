from .Helpers.types import *
from .Utils.write import Write
from .Utils.read import Read


def read_statement(compiler):
    Read(compiler).call()

    return compiler.commands.set_and_return_type(Types.INT)


def write_statement(compiler, aexp):
    value_type = aexp.compile_x86(compiler)
    compiler.commands.clean_type()
    Write(compiler).call(value_type)
