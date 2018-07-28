# -*- coding: utf-8 -*-

from .Core.commands import Commands
from .Core.registers import Registers


def assign_statement(compiler, node):
    """ Компиляция выражения присваивания """
    value_type = node.aexp.compile_asm(compiler)
    node.variable.context = 'assign'
    node.variable.type = value_type
    node.variable.compile_asm(compiler)


def compound_statement(compiler, node):
    """ Компиляция составного выражения """
    node.first.compile_asm(compiler)
    node.second.compile_asm(compiler)


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


def if_statement(compiler, node):
    """ Компиляция конструкции if с альтернативными ветками """
    skip_true_stmt_label = compiler.labels.create()

    node.condition.compile_asm(compiler)
    compiler.types.pop()
    # Если условие не выполнилось, пропускаем ветку.
    compiler.code.add(Commands.POP, Registers.EAX)\
        .add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, skip_true_stmt_label)
    node.true_stmt.compile_asm(compiler)
    compiler.code.add(Commands.POP, Registers.EAX)

    is_first_if = node.label_endif is None
    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if node.label_endif is None:
        node.label_endif = compiler.labels.create()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    compiler.code.add(Commands.JMP, node.label_endif)\
        .add_label(skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if node.alternatives_stmt:
        for alternative_stmt in node.alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.compile_asm(compiler)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if node.false_stmt:
        node.false_stmt.compile_asm(compiler)

    if is_first_if:
        compiler.code.add_label(node.label_endif)


def skip_statement(compiler, node):
    """ Компиляция оператора пропуска команды """
    compiler.code.add(Commands.NOP)
