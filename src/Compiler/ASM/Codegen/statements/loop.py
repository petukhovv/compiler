# -*- coding: utf-8 -*-

from ...Core.commands import Commands
from ...Core.registers import Registers


def repeat_statement(compiler, node):
    """ Компиляция repeat-until цикла """
    continue_label = compiler.labels.create()
    compiler.code.add_label(continue_label)
    node.body.compile_asm(compiler)
    node.condition.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, continue_label)


def while_statement(compiler, node):
    """ Компиляция while цикла """
    start_label = compiler.labels.create()
    compiler.code.add_label(start_label)
    finish_label = compiler.labels.create()

    node.condition.compile_asm(compiler)
    compiler.types.pop()
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, finish_label)
    node.body.compile_asm(compiler)
    # Делаем следующую итерацию
    compiler.code.add(Commands.JMP, start_label)\
        .add_label(finish_label)


def for_statement(compiler, node):
    """ Компиляция цикла for """
    start_label = compiler.labels.create()
    finish_label = compiler.labels.create()

    node.stmt1.compile_asm(compiler)
    compiler.code.add_label(start_label)
    node.stmt2.compile_asm(compiler)
    compiler.types.pop()
    # Если условия цикла не выполнилось, завешаем цикл
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, finish_label)
    node.body.compile_asm(compiler)
    node.stmt3.compile_asm(compiler)
    compiler.code.add(Commands.JMP, start_label)\
        .add_label(finish_label)
