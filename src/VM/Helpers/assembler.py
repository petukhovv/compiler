from src.VM.commands import *

from parser import command_class_relation_map, ARGS_SEPARATOR

commands_relation_map = dict((command_class_relation_map[k], k) for k in command_class_relation_map)

def assemble(command, argument = None):
    argument = '' if argument is None else ARGS_SEPARATOR + str(argument)
    return commands_relation_map[command] + argument
