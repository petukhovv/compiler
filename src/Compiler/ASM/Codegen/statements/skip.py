# -*- coding: utf-8 -*-

from ...Core.commands import Commands


def skip_statement(compiler, node):
    """ Компиляция оператора пропуска команды """
    compiler.code.add(Commands.NOP)
