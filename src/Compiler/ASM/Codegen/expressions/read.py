from ...Core.types import Types
from ...Runtime.read import Read


def read_statement(compiler, node):
    Read(compiler).call()
    return compiler.types.set(Types.INT)
