from parser import command_class_relation_map, ARGS_SEPARATOR

commands_relation_map = dict((command_class_relation_map[k], k) for k in command_class_relation_map)

def assemble(command, argument = ''):
    argument = '' if argument == '' else ARGS_SEPARATOR + str(argument)
    return commands_relation_map[command] + argument
