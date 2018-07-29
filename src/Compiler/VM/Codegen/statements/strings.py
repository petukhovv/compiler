# -*- coding: utf-8 -*-

from ...Deep.strings import StringCompiler


def strset(commands, data, node):
    """ Компиляция built-in функции strset (задание символа строки) """
    node.args.elements[2].compile_vm(commands, data)
    commands.clean_type()
    node.args.elements[1].compile_vm(commands, data)
    commands.clean_type()
    array_type = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strset(commands, data, array_type)
