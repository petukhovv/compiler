# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.arrays import *

AST = sys.modules['src.Parser.AST.arrays']

def unboxed_arrmake(commands, env, args):
    if len(args.elements) == 2:
        args_compile(args, 1, commands, env)
        # Если вторым аргументом был передан [], то дублируемым элементом будет 0 ( сигнатура: arrmake(n, []) )
        if isinstance(args.elements[1], AST.UnboxedArray) and len(args.elements[1].elements.elements) == 0:
            commands.add(Push, 0)
    args_compile(args, 0, commands, env)
    ArrayCompiler.unboxed_arrmake(commands, env, args.elements)
    # commands.add(Log, 0)
    # commands.add(Log, 1)
    # commands.add(Log, 2)

def unboxed(commands, env, elements):
    elements.compile_vm(commands, env)

def array_element(commands, env, array, index, other_indexes):
    array[index].compile_vm(commands, env)
