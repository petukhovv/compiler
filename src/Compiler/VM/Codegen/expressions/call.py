# -*- coding: utf-8 -*-

from ...Helpers.commands import Call


def call_statement(commands, data, node):
    """ Компиляция выражения вызова функции """
    for arg in node.args.elements:
        arg.compile_vm(commands, data)
    commands.add(Call, data.get_label(node.name))

    return data.get_return_type(node.name)
