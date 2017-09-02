# -*- coding: utf-8 -*-

from src.Parser.AST.base import *

from Helpers.string import *

def assign_statement(commands, env, variable, aexp):
    aexp.compile_vm(commands, env)
    # Тут надо писать в стор, если это строка, указатель на начало строки (а именно - номер соотв. переменной)
    # С этого номера символы идут подряд - читаем, пока не встретим 0.
    var_name = Env.var(env, variable.name)

    # Если значение требует хранения в heap memory, выделяем память и записываем его туда
    if isinstance(aexp, Heapable):
        String._store(commands, env)

    commands.add(Store, var_name)

def compound_statement(commands, env, first, second):
    first.compile_vm(commands, env)
    second.compile_vm(commands, env)

def repeat_statement(commands, env, condition, body):
    current_label = Env.label(env)
    commands.add(Label, current_label)
    body.compile_vm(commands, env)
    condition.compile_vm(commands, env)
    commands.add(Jz, current_label)

def while_statement(commands, env, condition, body):
    start_while_label = Env.label(env)
    commands.add(Label, start_while_label)
    end_while_label = Env.label(env)
    condition.compile_vm(commands, env)
    commands.add(Jz, end_while_label)
    body.compile_vm(commands, env)
    commands.add(Jump, start_while_label)\
        .add(Label, end_while_label)

def if_statement(commands, env, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    label_after_true_stmt = Env.label(env)
    condition.compile_vm(commands, env)

    # Если условие не выполнилось, пропускаем ветку.
    commands.add(Jz, label_after_true_stmt)
    true_stmt.compile_vm(commands, env)

    # Первая ветвь условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = Env.label(env)

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    commands.add(Jump, label_endif)\
        .add(Label, label_after_true_stmt)
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

def for_statement(commands, env, stmt1, stmt2, stmt3, body):
    start_for_label = Env.label(env)
    end_for_label = Env.label(env)
    stmt1.compile_vm(commands, env)
    commands.add(Label, start_for_label)
    stmt2.compile_vm(commands, env)
    commands.add(Jz, end_for_label)
    body.compile_vm(commands, env)
    stmt3.compile_vm(commands, env)
    commands.add(Jump, start_for_label)\
        .add(Label, end_for_label)

def skip_statement(commands, env):
    commands.add(Nop)
