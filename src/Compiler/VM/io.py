from src.VM.commands import *

def read_statement(commands, env):
    commands.add(Read)

def write_statement(commands, env, aexp):
    aexp.compile_vm(commands, env)
    commands.add(Write)
