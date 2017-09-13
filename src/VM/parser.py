from src.VM.commands import *
from pprint import pprint

COMMAND_SEPARATOR = '\n'
ARGS_SEPARATOR = ' '

def parse(program):
    commands = program.split(COMMAND_SEPARATOR)
    command_classes = []
    for command in commands:
        command = command.split(ARGS_SEPARATOR)
        args = []
        for arg in command[1:]:
            args.append(int(arg))
        command_classes.append(commands_map[command[0]](*args))

    return command_classes
