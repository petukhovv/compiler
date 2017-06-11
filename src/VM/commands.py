# -*- coding: utf-8 -*-

import sys

from pprint import pprint

from src.VM.Helpers.environment import Environment

"""
Перечисление команд стековой машины.
У каждой команды есть метод eval, который реализует её интерпретацию стековой машиной.
"""

""" Взятие значения со стека. """
class Push:
    def __init__(self, value):
        self.value = value

    def eval(self, commands, data, stack):
        stack.append(int(self.value))

""" Помещение значения в стек. """
class Pop:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')
        return stack.pop()

""" Отсутствие операции, команда пропускается. """
class Nop:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        pass

""" Помещение в стек значения переменной с именем name, взимаемой из памяти данных. """
class Load:
    def __init__(self, name):
        self.name = name

    def eval(self, commands, data, stack):
        value = Environment.search_variable(data, self.name)
        if value is None:
            raise RuntimeError('Unknown variable \'' + self.name + '\'')
        stack.append(value)

""" Сохранение значения переменной с именем name в память данных. """
class Store:
    def __init__(self, name):
        self.name = name

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')
        value = stack.pop()
        Environment.store_variable(data, self.name, value)

""" Взятие со стека двух чисел, их сложение и помещение результата обратно в стек. """
class Add:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = stack.pop()
        num2 = stack.pop()
        stack.append(num1 + num2)

""" Взятие со стека двух чисел, их умножение и помещение результата обратно в стек. """
class Mul:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = stack.pop()
        num2 = stack.pop()
        stack.append(num1 * num2)

""" Взятие со стека двух чисел, их вычитание и помещение результата обратно в стек. """
class Sub:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        num1 = stack.pop()
        num2 = stack.pop()
        stack.append(num2 - num1)

""" Взятие со стека двух чисел, их деление и помещение результата обратно в стек. """
class Div:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = stack.pop()
        num2 = stack.pop()
        stack.append(num2 / num1)

"""
Взятие со стека двух чисел, вычисление остатка от деления первого на второго
и помещение результата обратно в стек.
"""
class Mod:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = stack.pop()
        num2 = stack.pop()
        stack.append(num2 % num1)

""" Смена знака числа на вершине стека на противоположный. """
class Invert:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')
        num = stack.pop()
        stack.append(-num)

""" Взятие со стека двух чисел, их сравнение по коду сравнения и помещения результата сравнения обратно в стек. """
class Compare:
    def __init__(self, compare_code):
        self.compare_code = compare_code

    def eval(self, commands, data, stack):
        if len(stack) < 2:
            raise RuntimeError('Stack not contains two values')
        if self.compare_code not in [0, 1, 2, 3, 4, 5]:
            raise RuntimeError('Unknown compare code')
        num1 = stack.pop()
        num2 = stack.pop()
        result = 0
        if self.compare_code == 0 and num2 == num1:
            result = 1
        elif self.compare_code == 1 and num2 != num1:
            result = 1
        elif self.compare_code == 2 and num2 < num1:
            result = 1
        elif self.compare_code == 3 and num2 > num1:
            result = 1
        elif self.compare_code == 4 and num2 <= num1:
            result = 1
        elif self.compare_code == 5 and num2 >= num1:
            result = 1
        stack.append(result)

""" Установка метки. """
class Label:
    def __init__(self, name):
        self.name = name

    def eval(self, commands, data, stack):
        data['labels'][self.name] = commands['current']

""" Выполнение перехода к заданной метке. """
class Jump:
    def __init__(self, label):
        self.label = label

    def eval(self, commands, data, stack):
        commands['current'] = data['labels'][self.label]

""" Выполнение перехода к заданной метке, если значение на вершине стека - 0. """
class Jz:
    def __init__(self, label):
        self.label = label

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')
        num = stack.pop()
        if num == 0:
            commands['current'] = data['labels'][self.label]

""" Выполнение перехода к заданной метке, если значение на вершине стека - 1. """
class Jnz:
    def __init__(self, label):
        self.label = label

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')
        num = stack.pop()
        if num == 1:
            commands['current'] = data['labels'][self.label]

""" Считывание значения из стандартного потока ввода (stdin) и помещение результата на вершину стека. """
class Read:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        value = sys.stdin.readline()
        sys.stdout.write('> ')
        stack.append(int(value))

""" Получение значения с вершина стека и его передача в стандартный поток вывода (stdout). """
class Write:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')
        value = stack.pop()
        sys.stdout.write(str(value) + '\n')

""" Создание и вход в новый environment с заданным набором переменных (variables). """
class Enter:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def eval(self, commands, data, stack):
        Environment.create(data)

""" Выход из текущего environment и переход в родительский. """
class Exit:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def eval(self, commands, data, stack):
        Environment.clear(data)

""" Осуществление вызова. """
class Call:
    def __init__(self, name):
        self.name = name

    def eval(self, commands, data, stack):
        if len(stack) == 0:
            raise RuntimeError('Stack is empty')

        label = data['labels'][self.name]
        data['call_stack'].append(commands['current'])
        commands['current'] = label
        Environment.create(data)

""" Осуществление возврата к месту вызова. """
class Return:
    def __init__(self): pass

    def eval(self, commands, data, stack):
        if len(data['call_stack']) == 0:
            raise RuntimeError('Call stack is empty')
        Environment.clear(data)
        commands['current'] = data['call_stack'].pop()