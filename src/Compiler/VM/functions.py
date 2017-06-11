# -*- coding: utf-8 -*-

from src.VM.commands import *
from src.VM.Helpers.assembler import *

from pprint import pprint


def function(commands, env, name, args, body):
    start_function = env['label_counter']
    env['labels_map'][name] = start_function
    env['label_counter'] += 1
    end_function = env['label_counter']
    env['label_counter'] += 1

    # При последовательном выполнение пропускаем выполнения тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже.
    commands.append(assemble(Jump, end_function))

    # На эту метку переходим при вызове.
    commands.append(assemble(Label, start_function))

    # Компилим конструкции изъятия из стека аргументов функции и записи их в environment.
    var_counters = []
    for arg in args.elements:
        var_counters.append(env['var_counter'])
        env['vars_map'][arg] = env['var_counter']
        env['var_counter'] += 1

    for arg in args.elements:
        var_counter = var_counters.pop()
        commands.append(assemble(Store, var_counter))

    # Компилим код тела функции.
    body.compile_vm(commands, env)

    # Компилим конструкцию возврата к месту вызова.
    commands.append(assemble(Return))

    commands.append(assemble(Label, end_function))

def return_statement(commands, env, expr):
    expr.compile_vm(commands, env)

def function_call_statement(commands, env, name, args):
    for arg in args.elements:
        arg.compile_vm(commands, env)
    label = env['labels_map'][name]
    commands.append(assemble(Call, label))
