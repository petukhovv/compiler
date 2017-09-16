# -*- coding: utf-8 -*-

from pprint import pprint

from ..types import *

""" Мапа соответствий: тип данных - место хранения его значений """
typesMap = {
    Types.STRING: lambda scope: scope.heap,
    Types.STRING_INLINE: lambda scope: scope.stack,
    Types.UNBOXED_ARR: lambda scope: scope.heap,
    Types.UNBOXED_ARR_INLINE: lambda scope: scope.stack
}

""" Класс для клонирования значений ссылочных типов данных """
class Clonner:
    """ Клонирование строк """
    @staticmethod
    def string(pointer, stack, string_type, source, target):
        heap_offset = pointer
        current_symbol = None
        start_pointer = len(target.heap)

        # Копируем символы из source в target пока не встретим конец строки (0)
        while current_symbol != 0:
            current_symbol = typesMap[string_type](source)[heap_offset]
            target.heap.append(current_symbol)
            heap_offset += 1

        # Записываем на стек тип данных и новый адрес строки в новом scope
        stack.append(Types.STRING)
        stack.append(start_pointer)

    """ Клонирование unboxed-массивов """
    @staticmethod
    def unboxed_array(pointer, stack, string_type, source, target):
        arrlen = typesMap[string_type](source)[pointer]
        start_pointer = len(target.heap)
        arr_counter = 0

        # Копируем элементы массива из source в target
        while arr_counter <= arrlen:
            current_symbol = typesMap[string_type](source)[pointer + arr_counter]
            target.heap.append(current_symbol)
            arr_counter += 1

        # Записываем на стек тип данных и новый адрес массива в новом scope
        stack.append(Types.UNBOXED_ARR)
        stack.append(start_pointer)

    """ Общий метод для клонирования """
    @staticmethod
    def clone(pointer, stack, object_type, source, target):
        if object_type == Types.STRING or object_type == Types.STRING_INLINE:
            Clonner.string(pointer, stack, object_type, source, target)
        else:
            Clonner.unboxed_array(pointer, stack, object_type, source, target)
