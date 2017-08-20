from src.VM.Helpers.parser import COMMAND_SEPARATOR as VM_COMMANDS_SEPARATOR
from assembler import Commands

def compile_vm(ast):
    commands = Commands()
    environment = {
        'var_counter': 1,
        'vars_map': {},
        'label_counter': 1,
        'labels_map': {}
    }
    ast.compile_vm(commands, environment)
    return VM_COMMANDS_SEPARATOR.join(commands)
