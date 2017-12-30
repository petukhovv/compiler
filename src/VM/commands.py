# -*- coding: utf-8 -*-

import sys
from math import floor

"""
Перечисление команд стековой машины.
У каждой команды есть метод eval, который реализует её интерпретацию стековой машиной.
"""


class Push:
    """ Взятие значения со стека. """
    def __init__(self, value):
        self.value = value

    def eval(self, vm):
        vm.stack.append(int(self.value))


class Pop:
    """ Помещение значения в стек. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        return vm.stack.pop()


class Dup:
    """ Помещение значения в стек. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        vm.stack.append(vm.stack[-1])


class Nop:
    """ Отсутствие операции, команда пропускается. """
    def __init__(self): pass

    def eval(self, vm):
        pass


class Load:
    """ Помещение в стек значения переменной с адресом address, взимаемой из стековой памяти данных. """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        value = vm.scope().stack[self.address]
        if value is None:
            raise RuntimeError('Unknown variable \'' + str(self.address) + '\'')
        vm.stack.append(value)


class BLoad:
    """
    Помещение в стек значение переменной с адресом address, взимаемой из стековой памяти данных,
    который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
    """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        address = self.address + vm.stack.pop()
        value = vm.scope().stack[address]
        if value is None:
            raise RuntimeError('Unknown variable \'' + str(self.address) + '\'')
        vm.stack.append(value)


class DLoad:
    """ Помещение в стек значение переменной с адресом address, взимаемой из кучи. """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        value = vm.heap[self.address]
        if value is None:
            raise RuntimeError('Unknown variable \'' + str(self.address) + '\'')
        vm.stack.append(value)


class DBLoad:
    """
    Помещение в стек значение переменной с адресом address, взимаемой из кучи,
    который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
    """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        address = self.address + vm.stack.pop()
        value = vm.heap[address]
        vm.stack.append(value)


class Store:
    """ Сохранение значения переменной с адресом address в стекуовую память данных. """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        vm.scope().stack[self.address] = vm.stack.pop()


class BStore:
    """
    Сохранение значения переменной с адресом address в стековую памяти данных,
    который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
    """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')

        address = self.address + vm.stack.pop()
        vm.scope().stack[address] = vm.stack.pop()


class DStore:
    """ Сохранение значения переменной с адресом address в кучу. """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')

        vm.heap[self.address] = vm.stack.pop()


class DBStore:
    """
    Сохранение значения переменной с адресом address в кучу,
    который расчитывается по следующему правилу: <адрес в памяти> = <переданный адрес> + <значение с вершины стека>.
    """
    def __init__(self, address):
        self.address = address

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')

        address = self.address + vm.stack.pop()
        vm.heap[address] = vm.stack.pop()


class Add:
    """ Взятие со стека двух чисел, их сложение и помещение результата обратно в стек. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1 + num2)


class Mul:
    """ Взятие со стека двух чисел, их умножение и помещение результата обратно в стек. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1 * num2)


class Sub:
    """ Взятие со стека двух чисел, их вычитание и помещение результата обратно в стек. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 - num1)


class Div:
    """ Взятие со стека двух чисел, их деление и помещение результата обратно в стек. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(floor(num2 / num1))


class Mod:
    """
    Взятие со стека двух чисел, вычисление остатка от деления первого на второго
    и помещение результата обратно в стек.
    """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) < 2:
            raise RuntimeError('Stack not contains two values')
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 % num1)


class Invert:
    """ Смена знака числа на вершине стека на противоположный. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        num = vm.stack.pop()
        vm.stack.append(-num)


class Compare:
    """ Взятие со стека двух чисел, их сравнение по коду сравнения и помещения результата сравнения обратно в стек. """
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


class Label:
    """ Установка метки. """
    def __init__(self, name):
        self.name = name

    def eval(self, vm):
        vm.labels[self.name] = vm.commands.current


class Function(Label):
    """
    Пометка начала функции.
    Тоже самое, что и метка. Отдельный класс используются для расчетов размера стековой памяти перед запуском.
    """
    pass


class Jump:
    """ Выполнение безусловного перехода к заданной метке. """
    def __init__(self, label):
        self.label = label

    def eval(self, vm):
        vm.commands.current = vm.labels[self.label]


class Jz:
    """ Выполнение перехода к заданной метке, если значение на вершине стека - 0. """
    def __init__(self, label):
        self.label = label

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        num = vm.stack.pop()
        if num == 0:
            vm.commands.current = vm.labels[self.label]


class Jnz:
    """ Выполнение перехода к заданной метке, если значение на вершине стека - 1. """
    def __init__(self, label):
        self.label = label

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        num = vm.stack.pop()
        if num == 1:
            vm.commands.current = vm.labels[self.label]


class Read:
    """ Считывание значения из стандартного потока ввода (stdin) и помещение результата на вершину стека. """
    def __init__(self): pass

    def eval(self, vm):
        value = sys.stdin.readline()
        sys.stdout.write('> ')
        vm.stack.append(int(value))


class Write:
    """ Получение значения с вершина стека и его передача в стандартный поток вывода (stdout). """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.stack) == 0:
            raise RuntimeError('Stack is empty')
        value = vm.stack.pop()
        sys.stdout.write(str(value) + '\n')


class Enter:
    """ Создание и вход в новый scope с заданным набором переменных (variables). """
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def eval(self, vm):
        vm.create_scope()


class Exit:
    """ Выход из текущего scope и переход в вышестоящий. """
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def eval(self, vm):
        vm.remove_scope()


class Call:
    """ Осуществление вызова. """
    def __init__(self, name):
        self.name = name

    def eval(self, vm):
        vm.create_scope(self.name)

        # Наращиваем call stack и переходим к нужной метке
        vm.call_stack.append(vm.commands.current)
        vm.commands.current = vm.labels[self.name]


class Return:
    """ Осуществление возврата к месту вызова. """
    def __init__(self): pass

    def eval(self, vm):
        if len(vm.call_stack) == 0:
            raise RuntimeError('Call stack is empty')
        # Удаляем точку вызова из call stack'а, переходим к нужной метке и удаляем внутренний scope функции
        vm.commands.current = vm.call_stack.pop()
        vm.remove_scope()


class Malloc:
    """ Выделение в куче памяти заданного размера. """
    def __init__(self, size):
        self.size = size

    def eval(self, vm):
        start_data_pointer = len(vm.heap)
        i = 0
        while i < self.size:
            vm.heap.append(None)
            i += 1
        vm.stack.append(start_data_pointer)


class DMalloc:
    """
    Выделение памяти заданного размера,
    который расчитывается по следующему правилу: <размер> = <переданный размер> + <значение с вершины стека>.
    """
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


class Log:
    """ Служебная комманда для логирования (выводит содержимое стека или памяти на консоль). """
    def __init__(self, type):
        self.type = type

    def eval(self, vm):
        scope = vm.scope()
        if self.type == 0:
            print(vm.stack)
        elif self.type == 1:
            print('========== Log start (stack memory) ===========')
            i = 0
            for item in scope.stack:
                print(str(i) + ': ' + str(item))
                i += 1
            print('==========  Log end (stack memory)  ===========')
        elif self.type == 2:
            print('========== Log start (heap memory) ===========')
            i = 0
            for item in vm.heap:
                print(str(i) + ': ' + str(item))
                i += 1
            print('==========  Log end (heap memory)  ===========')
