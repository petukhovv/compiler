# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop

class ArrayCompiler:
    @staticmethod
    def unboxed_arrmake(commands, env, args):
        arr_pointer = env.var()
        arr_length = env.var()

        finish_label = env.label()

        commands.add(Dup)
        # Сохраняем длину массива в переменную
        commands.add(Store, arr_length)

        commands.add(DAllocate, 0)
        # Сохраняем длину массива в переменную
        commands.add(Store, arr_pointer)

        if len(args) == 2:
            basis_element = env.var()

            # Сохраняем длину массива в переменную
            commands.add(Store, basis_element)

            def cycle_body(_counter, b, c):
                commands.add(Load, _counter)
                commands.add(Load, arr_length)
                commands.add(Compare, 5)
                commands.add(Jnz, finish_label)
                commands.add(Load, basis_element)
                dbstore(arr_pointer, _counter, commands)
            counter = Loop.simple(commands, env, cycle_body, return_counter=True)

        commands.add(Label, finish_label)
