from src.VM.commands import *
from src.VM.Helpers.assembler import *

def read_statement(commands, env):
    commands.append(assemble(Read))

def write_statement(commands, env, aexp):
    aexp.compile_vm(commands, env)
    commands.append(assemble(Write))
