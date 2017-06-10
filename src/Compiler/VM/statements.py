from src.VM.commands import *
from src.VM.Helpers.assembler import *

from pprint import pprint

def assign_statement(commands, env, variable, aexp):
    aexp.compile_vm(commands, env)
    if variable.name in env['vars_map']:
        commands.append(assemble(Store, env['vars_map'][variable.name]))
    else:
        env['vars_map'][variable.name] = env['var_counter']
        commands.append(assemble(Store, env['var_counter']))
        env['var_counter'] += 1

def compound_statement(commands, env, first, second):
    first.compile_vm(commands, env)
    second.compile_vm(commands, env)

def repeat_statement(commands, env, condition, body):
    commands.append(assemble(Label, env['label_counter']))
    current_label = env['label_counter']
    env['label_counter'] += 1
    body.compile_vm(commands, env)
    condition.compile_vm(commands, env)
    commands.append(assemble(Jz, current_label))

def while_statement(commands, env, condition, body):
    start_while_label = env['label_counter']
    commands.append(assemble(Label, start_while_label))
    env['label_counter'] += 1
    end_while_label = env['label_counter']
    env['label_counter'] += 1
    condition.compile_vm(commands, env)
    commands.append(assemble(Jz, end_while_label))
    body.compile_vm(commands, env)
    commands.append(assemble(Jump, start_while_label))
    commands.append(assemble(Label, end_while_label))
