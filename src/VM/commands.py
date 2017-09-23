# -*- coding: utf-8 -*-

import sys

from pprint import pprint

"""
Перечисление команд стековой машины.
У каждой команды есть метод eval, который реализует её интерпретацию стековой машиной.
"""

""" Взятие значения со стека. """
class Push:
    def __init__(self, value):
        self.value = value

    def eval(self, vm):
        vm.stack.append(int(self.value))

""" Помещение значения в стек. """
class Pop:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        return vm.stack.pop()

""" Помещение значения в стек. """
class Dup:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        vm.stack.append(vm.stack[-1])

""" Отсутствие операции, команда пропускается. """
class Nop:
    def __init__(self): pass

    def eval(self, vm):
        pass

""" Помещение в стек значения переменной с адресом address, взимаемой из стековой памяти данных. """
class Load:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        value = vm.scope().stack[self.address]
        if value is None:
            raise RuntimeError('Unknown variable \'' + str(self.address) + '\'')
        vm.stack.append(value)

"""
Помещение в стек значение переменной с адресом address, взимаемой из стековой памяти данных,
который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
"""
class BLoad:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        address = self.address + vm.stack.pop()
        value = vm.scope().stack[address]
        if value is None:
            raise RuntimeError('Unknown variable \'' + str(self.address) + '\'')
        vm.stack.append(value)

""" Помещение в стек значение переменной с адресом address, взимаемой из кучи. """
class DLoad:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        value = vm.heap[self.address]
        if value is None:
            raise RuntimeError('Unknown variable \'' + str(self.address) + '\'')
        vm.stack.append(value)

"""
Помещение в стек значение переменной с адресом address, взимаемой из кучи,
который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
"""
class DBLoad:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        address = self.address + vm.stack.pop()
        value = vm.heap[address]
        vm.stack.append(value)

""" Сохранение значения переменной с адресом address в стекуовую память данных. """
class Store:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        vm.scope().stack[self.address] = vm.stack.pop()

"""
Сохранение значения переменной с адресом address в стековую памяти данных,
который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
"""
class BStore:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')

        address = self.address + vm.stack.pop()
        vm.scope().stack[address] = vm.stack.pop()

""" Сохранение значения переменной с адресом address в кучу. """
class DStore:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')

        vm.heap[self.address] = vm.stack.pop()

"""
Сохранение значения переменной с адресом address в кучу,
который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
"""
class DBStore:
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')

        address = self.address + vm.stack.pop()
        vm.heap[address] = vm.stack.pop()

""" Взятие со стека двух чисел, их сложение и помещение результата обратно в стек. """
class Add:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1 + num2)

""" Взятие со стека двух чисел, их умножение и помещение результата обратно в стек. """
class Mul:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1 * num2)

""" Взятие со стека двух чисел, их вычитание и помещение результата обратно в стек. """
class Sub:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 - num1)

""" Взятие со стека двух чисел, их деление и помещение результата обратно в стек. """
class Div:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 / num1)

"""
Взятие со стека двух чисел, вычисление остатка от деления первого на второго
и помещение результата обратно в стек.
"""
class Mod:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 % num1)

""" Смена знака числа на вершине стека на противоположный. """
class Invert:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        num = vm.stack.pop()
        vm.stack.append(-num)

""" Взятие со стека двух чисел, их сравнение по коду сравнения и помещения результата сравнения обратно в стек. """
class Compare:
    def __init__(self, compare_code):
        self.compare_code = compare_code

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        if self.compare_code not in [0, 1, 2, 3, 4, 5]:
            raise RuntimeError('Unknown compare code')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
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
        vm.stack.append(result)

""" Установка метки. """
class Label:
    def __init__(self, name):
        self.name = name

    def eval(self, vm):
        vm.labels[self.name] = vm.commands.current

"""
Пометка начала функции.
Тоже самое, что и метка. Отдельный класс используются для расчетов размера стековой памяти перед запуском.
"""
class Function(Label): pass

""" Выполнение безусловного перехода к заданной метке. """
class Jump:
    def __init__(self, label):
        self.label = label

    def eval(self, vm):
        vm.commands.current = vm.labels[self.label]

""" Выполнение перехода к заданной метке, если значение на вершине стека - 0. """
class Jz:
    def __init__(self, label):
        self.label = label

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        num = vm.stack.pop()
        if num == 0:
            vm.commands.current = vm.labels[self.label]

""" Выполнение перехода к заданной метке, если значение на вершине стека - 1. """
class Jnz:
    def __init__(self, label):
        self.label = label

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        num = vm.stack.pop()
        if num == 1:
            vm.commands.current = vm.labels[self.label]

""" Считывание значения из стандартного потока ввода (stdin) и помещение результата на вершину стека. """
class Read:
    def __init__(self): pass

    def eval(self, vm):
        value = sys.stdin.readline()
        sys.stdout.write('> ')
        vm.stack.append(int(value))

""" Получение значения с вершина стека и его передача в стандартный поток вывода (stdout). """
class Write:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        value = vm.stack.pop()
        sys.stdout.write(str(value) + '\n')

""" Создание и вход в новый scope с заданным набором переменных (variables). """
class Enter:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def eval(self, vm):
        vm.create_scope()

""" Выход из текущего scope и переход в вышестоящий. """
class Exit:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def eval(self, vm):
        vm.remove_scope()

""" Осуществление вызова. """
class Call:
    def __init__(self, name):
        self.name = name

    def eval(self, vm):
        vm.create_scope(self.name)

        # Наращиваем call stack и переходим к нужной метке
        vm.call_stack.append(vm.commands.current)
        vm.commands.current = vm.labels[self.name]

""" Осуществление возврата к месту вызова. """
class Return:
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.call_stack) == 0:
            raise RuntimeError('Call stack is empty')
        # Удаляем точку вызова из call stack'а, переходим к нужной метке и удаляем внутренний scope функции
        vm.commands.current = vm.call_stack.pop()
        vm.remove_scope()

""" Выделение в куче памяти заданного размера. """
class Allocate:
    def __init__(self, size):
        self.size = size

    def eval(self, vm):
        start_data_pointer = len(vm.heap)
        i = 0
        while i < self.size:
            vm.heap.append(None)
            i += 1
        vm.stack.append(start_data_pointer)

"""
Выделение памяти заданного размера,
который расчитывается по следующему правилу: <размер> = <переданный размер> + <значение с вершины стека>.
"""
class DAllocate:
    def __init__(self, size):
        self.size = size

    def eval(self, vm):
        start_data_pointer = len(vm.heap)
        memory_size = self.size + vm.stack.pop()
        i = 0
        while i < memory_size:
            vm.heap.append(None)
            i += 1
        vm.stack.append(start_data_pointer)

""" Служебная комманда для логирования (выводит содержимое стека или памяти на консоль). """
class Log:
    def __init__(self, type):
        self.type = type

    def eval(self, vm):
        scope = vm.scope()
        if self.type == 0:
            pprint(vm.stack)
        elif self.type == 1:
            print '========== Log start (stack memory) ==========='
            i = 0
            for item in scope.stack:
                print str(i) + ': ' + str(item)
                i += 1
            print '==========  Log end (stack memory)  ==========='
        elif self.type == 2:
            print '========== Log start (heap memory) ==========='
            i = 0
            for item in vm.heap:
                print str(i) + ': ' + str(item)
                i += 1
            print '==========  Log end (heap memory)  ==========='
