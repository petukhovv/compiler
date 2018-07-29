from ...Helpers.types import Types
from ...Helpers.commands import Read


def read_statement(commands, data, node):
    commands.add(Read)

    return commands.set_and_return_type(Types.INT)
