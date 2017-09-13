class types:
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

PRIMITIVE_TYPES = [
    types.NONE,
    types.INT,
    types.CHAR,
    types.BOOL
]

STACKABLE_TYPES = [
    types.NONE,
    types.INT,
    types.CHAR,
    types.BOOL,
    types.BOXED_ARR_INLINE,
    types.UNBOXED_ARR_INLINE,
    types.STRING_INLINE
]

HEAPABLE_TYPES = [
    types.STRING,
    types.BOXED_ARR,
    types.UNBOXED_ARR,
    types.DYNAMIC
]
