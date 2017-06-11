# -*- coding: utf-8 -*-

from src.VM.commands import *
from src.VM.Helpers.assembler import *

from Helpers.environment import *

from pprint import pprint

def assign_statement(commands, env, variable, aexp):
    aexp.compile_vm(commands, env)
    if Environment.is_exist_var(env, variable.name):
        commands.append(assemble(Store, Environment.get_var(env, variable.name)))
    else:
        commands.append(assemble(Store, Environment.create_var(env, variable.name)))

def compound_statement(commands, env, first, second):
    first.compile_vm(commands, env)
    second.compile_vm(commands, env)

def repeat_statement(commands, env, condition, body):
    current_label = Environment.create_label(env)
    commands.append(assemble(Label, current_label))
    body.compile_vm(commands, env)
    condition.compile_vm(commands, env)
    commands.append(assemble(Jz, current_label))

def while_statement(commands, env, condition, body):
    start_while_label = Environment.create_label(env)
    commands.append(assemble(Label, start_while_label))
    end_while_label = Environment.create_label(env)
    condition.compile_vm(commands, env)
    commands.append(assemble(Jz, end_while_label))
    body.compile_vm(commands, env)
    commands.append(assemble(Jump, start_while_label))
    commands.append(assemble(Label, end_while_label))

def if_statement(commands, env, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    label_after_true_stmt = Environment.create_label(env)
    condition.compile_vm(commands, env)

    # Если условие не выполнилось, пропускаем ветку.
    commands.append(assemble(Jz, label_after_true_stmt))
    true_stmt.compile_vm(commands, env)

    # Первая ветвь условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = Environment.create_label(env)

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    commands.append(assemble(Jump, label_endif))
    commands.append(assemble(Label, label_after_true_stmt))
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

    commands.append(assemble(Label, label_endif))

def for_statement(commands, env, stmt1, stmt2, stmt3, body):
    start_for_label = Environment.create_label(env)
    end_for_label = Environment.create_label(env)
    stmt1.compile_vm(commands, env)
    commands.append(assemble(Label, start_for_label))
    stmt2.compile_vm(commands, env)
    commands.append(assemble(Jz, end_for_label))
    body.compile_vm(commands, env)
    stmt3.compile_vm(commands, env)
    commands.append(assemble(Jump, start_for_label))
    commands.append(assemble(Label, end_for_label))

def skip_statement(commands, env):
    commands.append(assemble(Nop))
