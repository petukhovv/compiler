from Helpers.base import *

def read_statement(commands, data):
    commands.add(Read)

    return commands.set_and_return_type(types.INT)

def write_statement(commands, data, aexp):
    aexp.compile_vm(commands, data)
    commands.extract_value()
    commands.add(Write)
