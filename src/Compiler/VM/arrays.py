# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.arrays import *

AST = sys.modules['src.Parser.AST.arrays']

def unboxed_arrmake(commands, env, args):
    if len(args.elements) == 2:
        args_compile(args, 1, commands, env)
        # Если вторым аргументом был передан [], то дублируемым элементом будет 0 ( сигнатура: arrmake(n, []) )
        is_array_default_values = isinstance(args.elements[1], AST.UnboxedArray)
        if is_array_default_values and len(args.elements[1].elements.elements) == 0:
            commands.add(Push, 0)
            values_type = 'zeros'
        elif is_array_default_values and len(args.elements[1].elements.elements) != 0:
            values_type = 'preset'
        else:
            values_type = 'repeated'
    else:
        values_type = 'none'
    args_compile(args, 0, commands, env)
    ArrayCompiler.unboxed_arrmake(commands, env, values_type)
    # commands.add(Log, 0)
    # commands.add(Log, 1)
    # commands.add(Log, 2)

def unboxed(commands, env, elements):
    arr_elements = elements.compile_vm(commands, env)
    # Кладем на стек строку
    for element in reversed(arr_elements):
        commands.add(Push, element)

def array_element(commands, env, array, index, other_indexes):
    index.compile_vm(commands, env)
    commands.add(Load, env.get_var(array))
    ArrayCompiler.element(commands, env)
