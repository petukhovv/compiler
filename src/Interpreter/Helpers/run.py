from src.VM.Helpers.parser import COMMAND_SEPARATOR as VM_COMMANDS_SEPARATOR

from environment import *

def interpret(ast):
    ast.eval(Environment().create())

def compile_vm(ast):
    commands = []
    environment = {
        'var_counter': 1,
        'vars_map': {}
    }
    ast.compile_vm(commands, environment)
    return VM_COMMANDS_SEPARATOR.join(commands)
