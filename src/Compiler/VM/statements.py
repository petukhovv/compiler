from src.VM.commands import *
from src.VM.Helpers.assembler import *

def assign_statement(commands, env, variable, aexp):
    aexp.compile_vm(commands, env)
    env['vars_map'][variable] = env['var_counter']
    commands.append(assemble(Store, env['var_counter']))
    env['var_counter'] += 1
