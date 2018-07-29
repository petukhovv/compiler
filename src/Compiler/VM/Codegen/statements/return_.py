# -*- coding: utf-8 -*-


def return_statement(commands, data, node):
    """ Компиляция выражения возврата к месту вызова """
    return_type = node.expr.compile_vm(commands, data)
    data.set_return_type(return_type)