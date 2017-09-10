from Helpers.base import *

def read_statement(commands, env):
    commands.add(Read)
    commands.set_return_type(types.INT)

def write_statement(commands, env, aexp):
    aexp.compile_vm(commands, env)
    commands.extract_value()
    commands.add(Write)
