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
    BOXED_ARR_INLINE = 7
    UNBOXED_ARR_INLINE = 8
    DYNAMIC = 9
    STRING_INLINE = 10

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
    Types.STRING_INLINE,
    Types.BOXED_ARR,
    Types.UNBOXED_ARR,
    Types.BOXED_ARR_INLINE,
    Types.UNBOXED_ARR_INLINE
]

""" Перечень типов, значения которых хранятся в стековой памяти """
STACKABLE_TYPES = [
    Types.NONE,
    Types.INT,
    Types.CHAR,
    Types.BOOL,
    Types.STRING_INLINE,
    Types.BOXED_ARR_INLINE,
    Types.UNBOXED_ARR_INLINE
]

""" Перечень типов, значения которых хранятся в куче """
HEAPABLE_TYPES = [
    Types.STRING,
    Types.BOXED_ARR,
    Types.UNBOXED_ARR
]
