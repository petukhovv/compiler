# -*- coding: utf-8 -*-

from src.VM.commands import *
from Helpers.environment import *

""" Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
def function(commands, env, name, args, body):
    start_function = env.label(name)
    finish_function = env.label()

    # При последовательном выполнении пропускаем выполнение тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже
    commands.add(Jump, finish_function)

    # На эту метку переходим при вызове
    commands.add(Label, start_function)

    # Для всех аргументов создаем переменные
    arg_names = []
    for arg in args.elements:
        arg_names.append(env.var(arg))

    # Компилируем конструкции изъятия из стека (в обратном порядке) аргументов функции и записи их в environment
    for _ in args.elements:
        commands.add(Store, arg_names.pop())

    # Компилируем код тела функции
    body.compile_vm(commands, env)

    # Компилируем конструкцию возврата к месту вызова
    commands.add(Return)\
        .add(Label, finish_function)

""" Компиляция выражения возврата к месту вызова """
def return_statement(commands, env, expr):
    expr.compile_vm(commands, env)

""" Компиляция выражения вызова функции """
def call_statement(commands, env, name, args):
    for arg in args.elements:
        arg.compile_vm(commands, env)
    commands.add(Call, env.get_label(name))
