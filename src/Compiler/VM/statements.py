# -*- coding: utf-8 -*-

from src.VM.commands import *
from src.VM.Helpers.assembler import *

from pprint import pprint

def assign_statement(commands, env, variable, aexp):
    aexp.compile_vm(commands, env)
    if variable.name in env['vars_map']:
        commands.append(assemble(Store, env['vars_map'][variable.name]))
    else:
        env['vars_map'][variable.name] = env['var_counter']
        commands.append(assemble(Store, env['var_counter']))
        env['var_counter'] += 1

def compound_statement(commands, env, first, second):
    first.compile_vm(commands, env)
    second.compile_vm(commands, env)

def repeat_statement(commands, env, condition, body):
    commands.append(assemble(Label, env['label_counter']))
    current_label = env['label_counter']
    env['label_counter'] += 1
    body.compile_vm(commands, env)
    condition.compile_vm(commands, env)
    commands.append(assemble(Jz, current_label))

def while_statement(commands, env, condition, body):
    start_while_label = env['label_counter']
    commands.append(assemble(Label, start_while_label))
    env['label_counter'] += 1
    end_while_label = env['label_counter']
    env['label_counter'] += 1
    condition.compile_vm(commands, env)
    commands.append(assemble(Jz, end_while_label))
    body.compile_vm(commands, env)
    commands.append(assemble(Jump, start_while_label))
    commands.append(assemble(Label, end_while_label))

def if_statement(commands, env, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    label_after_true_stmt = env['label_counter']
    env['label_counter'] += 1
    condition.compile_vm(commands, env)
    # Если условие не выполнилось, пропускаем ветку.
    commands.append(assemble(Jz, label_after_true_stmt))
    true_stmt.compile_vm(commands, env)
    # Первая ветвь условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = env['label_counter']
        env['label_counter'] += 1
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
