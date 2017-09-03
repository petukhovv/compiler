# -*- coding: utf-8 -*-

from Helpers.string import *

""" Компиляция выражения присваивания """
def assign_statement(commands, env, variable, aexp):
    aexp.compile_vm(commands, env)
    commands.add(Store, Env.var(env, variable.name))

""" Компиляция составного выражения """
def compound_statement(commands, env, first, second):
    first.compile_vm(commands, env)
    second.compile_vm(commands, env)

""" Компиляция repeat-until цикла """
def repeat_statement(commands, env, condition, body):
    continue_label = Env.label(env)
    commands.add(Label, continue_label)
    body.compile_vm(commands, env)
    condition.compile_vm(commands, env)
    # Если после очередной итерации условие останова не выполнилось, делаем следующую итерацию
    commands.add(Jz, continue_label)

""" Компиляция while цикла """
def while_statement(commands, env, condition, body):
    start_label = Env.label(env)
    commands.add(Label, start_label)
    finish_label = Env.label(env)
    condition.compile_vm(commands, env)
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    commands.add(Jz, finish_label)
    body.compile_vm(commands, env)
    # Делаем следующую итерацию
    commands.add(Jump, start_label)\
        .add(Label, finish_label)

""" Компиляция конструкции if с альтернативными ветками """
def if_statement(commands, env, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    skip_true_stmt_label = Env.label(env)

    condition.compile_vm(commands, env)
    # Если условие не выполнилось, пропускаем ветку.
    commands.add(Jz, skip_true_stmt_label)
    true_stmt.compile_vm(commands, env)

    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = Env.label(env)

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    commands.add(Jump, label_endif)\
        .add(Label, skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if alternatives_stmt:
        for alternative_stmt in alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.compile_vm(commands, env, label_endif)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if false_stmt:
        false_stmt.compile_vm(commands, env)

    commands.add(Label, label_endif)

""" Компиляция цикла for """
def for_statement(commands, env, stmt1, stmt2, stmt3, body):
    start_label = Env.label(env)
    finish_label = Env.label(env)

    stmt1.compile_vm(commands, env)
    commands.add(Label, start_label)
    stmt2.compile_vm(commands, env)
    # Если условия цикла не выполнилось, завешаем цикл
    commands.add(Jz, finish_label)
    body.compile_vm(commands, env)
    stmt3.compile_vm(commands, env)
    commands.add(Jump, start_label)\
        .add(Label, finish_label)

""" Компиляция оператора пропуска команды """
def skip_statement(commands, env):
    commands.add(Nop)
