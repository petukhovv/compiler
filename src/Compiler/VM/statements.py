# -*- coding: utf-8 -*-

from .Deep.arrays import *


def assign_statement(commands, data, node):
    """ Компиляция выражения присваивания """
    value_type = node.aexp.compile_vm(commands, data)
    commands.clean_type()
    node.variable.context = 'assign'
    node.variable.type = value_type
    node.variable.compile_vm(commands, data)


def compound_statement(commands, data, node):
    """ Компиляция составного выражения """
    node.first.compile_vm(commands, data)
    node.second.compile_vm(commands, data)


def repeat_statement(commands, data, node):
    """ Компиляция repeat-until цикла """
    continue_label = data.label()
    commands.add(Label, continue_label)
    node.body.compile_vm(commands, data)
    node.condition.compile_vm(commands, data)
    commands.clean_type()
    # Если после очередной итерации условие останова не выполнилось, делаем следующую итерацию
    commands.add(Jz, continue_label)


def while_statement(commands, data, node):
    """ Компиляция while цикла """
    start_label = data.label()
    commands.add(Label, start_label)
    finish_label = data.label()
    node.condition.compile_vm(commands, data)
    commands.clean_type()
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    commands.add(Jz, finish_label)
    node.body.compile_vm(commands, data)
    # Делаем следующую итерацию
    commands.add(Jump, start_label)\
        .add(Label, finish_label)


def for_statement(commands, data, node):
    """ Компиляция цикла for """
    start_label = data.label()
    finish_label = data.label()

    node.stmt1.compile_vm(commands, data)
    commands.add(Label, start_label)
    node.stmt2.compile_vm(commands, data)
    commands.clean_type()
    # Если условия цикла не выполнилось, завешаем цикл
    commands.add(Jz, finish_label)
    node.body.compile_vm(commands, data)
    node.stmt3.compile_vm(commands, data)
    commands.add(Jump, start_label)\
        .add(Label, finish_label)


def if_statement(commands, data, node):
    """ Компиляция конструкции if с альтернативными ветками """
    skip_true_stmt_label = data.label()

    node.condition.compile_vm(commands, data)
    commands.clean_type()
    # Если условие не выполнилось, пропускаем ветку.
    commands.add(Jz, skip_true_stmt_label)
    node.true_stmt.compile_vm(commands, data)

    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if node.label_endif is None:
        node.label_endif = data.label()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    commands.add(Jump, node.label_endif)\
        .add(Label, skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if node.alternatives_stmt:
        for alternative_stmt in node.alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.label_endif = node.label_endif
            alternative_stmt.compile_vm(commands, data)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if node.false_stmt:
        node.false_stmt.compile_vm(commands, data)

    commands.add(Label, node.label_endif)


def skip_statement(commands, data, node):
    """ Компиляция оператора пропуска команды """
    commands.add(Nop)
