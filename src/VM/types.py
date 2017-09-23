# -*- coding: utf-8 -*-

""" Перечень типов виртуальной машины """
class Types:
    NONE = 0
    INT = 1
    CHAR = 2
    BOOL = 3
    STRING = 4
    BOXED_ARR = 5
    UNBOXED_ARR = 6
    DYNAMIC = 9

""" Перечень примитивных типов """
PRIMITIVE_TYPES = [
    Types.NONE,
    Types.INT,
    Types.CHAR,
    Types.BOOL
]

""" Перечень ссылочных типов """
POINTER_TYPES = [
    Types.STRING,
    Types.BOXED_ARR,
    Types.UNBOXED_ARR
]

""" Перечень типов, значения которых хранятся в стековой памяти """
STACKABLE_TYPES = [
    Types.NONE,
    Types.INT,
    Types.CHAR,
    Types.BOOL
]

""" Перечень типов, значения которых хранятся в куче """
HEAPABLE_TYPES = [
    Types.STRING,
    Types.BOXED_ARR,
    Types.UNBOXED_ARR
]
