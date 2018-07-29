# -*- coding: utf-8 -*-


def assign_statement(commands, data, node):
    """ Компиляция выражения присваивания """
    value_type = node.aexp.compile_vm(commands, data)
    commands.clean_type()
    node.variable.context = 'assign'
    node.variable.type = value_type
    node.variable.compile_vm(commands, data)
