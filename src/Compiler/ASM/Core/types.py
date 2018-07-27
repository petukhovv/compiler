from .commands import Commands


class Types:
    NOTHING = 0
    INT = 1
    CHAR = 2
    BOOL = 3
    STRING = 4
    BOXED_ARR = 5
    UNBOXED_ARR = 6
    REFERENCE = 7

    SIZE = 4

    def __init__(self, compiler):
        self.compiler = compiler

    def get_static_type(self, value):
        if isinstance(value, str):
            return Types.CHAR
        elif isinstance(value, int):
            return Types.INT
        else:
            return Types.NOTHING

    def set(self, value_type):
        self.compiler.code.add(Commands.PUSH, value_type)

        return value_type

    def pop(self):
        self.compiler.code.stack_pop()
