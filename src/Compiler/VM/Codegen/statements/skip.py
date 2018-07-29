# -*- coding: utf-8 -*-

from ...Helpers.commands import Nop


def skip_statement(commands, data, node):
    """ Компиляция оператора пропуска команды """
    commands.add(Nop)
