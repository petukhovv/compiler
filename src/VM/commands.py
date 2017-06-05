# -*- coding: utf-8 -*-

"""
Перечисление команд стековой машины.
У каждой команды есть метод eval, который реализует её интерпретацию стековой машиной.
"""

""" Взятие значения со стека. """
class Push:
    def __init__(self, value):
        self.value = value

""" Помещение значения в стек. """
class Pop:
    def __init__(self): pass

""" Отсутствие операции, команда пропускается. """
class Nop: pass

""" Прекращение выполнения программы. """
class Stop:
    def __init__(self): pass

""" Помещение в стек значения переменной с именем name, взимаемой из памяти данных. """
class Load:
    def __init__(self, name):
        self.name = name

""" Сохранение значения переменной с именем name в память данных. """
class Store:
    def __init__(self, name):
        self.name = name

""" Взятие со стека двух чисел, их сложение и помещение результата обратно в стек. """
class Add:
    def __init__(self): pass

""" Взятие со стека двух чисел, их умножение и помещение результата обратно в стек. """
class Mul:
    def __init__(self): pass

""" Взятие со стека двух чисел, их вычитание и помещение результата обратно в стек. """
class Sub:
    def __init__(self): pass

""" Взятие со стека двух чисел, их деление и помещение результата обратно в стек. """
class Div:
    def __init__(self): pass

""" Смена знака числа на вершине стека на противоположный. """
class Invert:
    def __init__(self): pass

""" Взятие со стека двух чисел, их сравнение по коду сравнения и помещения результата сравнения обратно в стек. """
class Compare:
    def __init__(self, compare_code):
        self.compare_code = compare_code

""" Установка метки. """
class Label:
    def __init__(self, name):
        self.name = name

""" Выполнение перехода к заданной метке. """
class Jump:
    def __init__(self, label):
        self.label = label

""" Выполнение перехода к заданной метке, если значение на вершине стека - 0. """
class Jz:
    def __init__(self, label):
        self.label = label

""" Выполнение перехода к заданной метке, если значение на вершине стека - 1. """
class Jnz:
    def __init__(self, label):
        self.label = label

""" Получение значения с вершина стека и его передача в стандартный поток вывода (stdout). """
class Write:
    def __init__(self): pass

""" Считывание значения из стандартного потока ввода (stdin) и помещение результата на вершину стека. """
class Read:
    def __init__(self): pass

""" Создание и вход в новый environment с заданным набором переменных (variables). """
class Enter:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

""" Осуществление вызова. """
class Call:
    def __init__(self, name):
        self.name = name

""" Осуществление возврата к месту вызова. """
class Return:
    def __init__(self): pass
