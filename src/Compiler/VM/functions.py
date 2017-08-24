# -*- coding: utf-8 -*-

from src.VM.commands import *

from Helpers.environment import *

def function(commands, env, name, args, body):
    start_function = Environment.create_label(env, name)
    end_function = Environment.create_label(env)

    # При последовательном выполнение пропускаем выполнения тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже.
    commands.add(Jump, end_function)

    # На эту метку переходим при вызове.
    commands.add(Label, start_function)

    # Компилим конструкции изъятия из стека аргументов функции и записи их в environment.
    var_counters = []
    for arg in args.elements:
        var_counters.append(Environment.create_var(env, arg))

    for arg in args.elements:
        var_counter = var_counters.pop()
        commands.add(Store, var_counter)

    # Компилим код тела функции.
    body.compile_vm(commands, env)

    # Компилим конструкцию возврата к месту вызова.
    commands.add(Return)\
        .add(Label, end_function)

def return_statement(commands, env, expr):
    expr.compile_vm(commands, env)

def function_call_statement(commands, env, name, args):
    for arg in args.elements:
        arg.compile_vm(commands, env)
    label = Environment.get_label(env, name)
    commands.add(Call, label)
