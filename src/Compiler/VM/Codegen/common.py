def enumeration(commands, data, node):
    return node.elements


def compound_statement(commands, data, node):
    """ Компиляция составного выражения """
    node.first.compile_vm(commands, data)
    node.second.compile_vm(commands, data)
