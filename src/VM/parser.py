from pprint import pprint

from src.VM.commands import *

COMMAND_SEPARATOR = '\n'
ARGS_SEPARATOR = ' '

command_class_relation_map = {
    'PUSH': Push,
    'POP': Pop,
    'NOP': Nop,
    'LOAD': Load,
    'STORE': Store,
    'ADD': Add,
    'MUL': Mul,
    'SUB': Sub,
    'DIV': Div,
    'INVERT': Invert,
    'COMPARE': Compare,
    'LABEL': Label,
    'JUMP': Jump,
    'JZ': Jz,
    'JNZ': Jnz,
    'READ': Read,
    'WRITE': Write,
    'ENTER': Enter,
    'CALL': Call,
    'RETURN': Return
}

def parse(program):
    commands = program.split(COMMAND_SEPARATOR)
    command_classes = []
    for command in commands:
        command = command.split(ARGS_SEPARATOR)
        args = []
        for arg in command[1:]:
            args.append(int(arg))
        command_classes.append(command_class_relation_map[command[0]](*args))

    return command_classes
