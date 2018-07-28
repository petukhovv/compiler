from Parser.AST.arithmetic_exprs import *

from Compiler.VM import arrays as compile_vm
from Compiler.ASM import arrays as compile_asm
from Interpreter import arrays as interpreter

from .base import AST

CLASS = "arrays"


class UnboxedArray(AST):
    pointers = 0

    def __init__(self, elements):
        super().__init__(CLASS, "arrmake_inline")

        self.elements = elements
        self.children = [elements]
        self.type = 'unboxed'

    def interpret(self, env):
        return interpreter.unboxed_array(env, self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake_inline(commands, data, self.elements, 'unboxed')


class BoxedArray(AST):
    pointers = 0

    def __init__(self, elements):
        super().__init__(CLASS, "arrmake_inline")

        self.elements = elements
        self.children = [elements]
        self.type = 'boxed'

    def interpret(self, env):
        return interpreter.boxed_array(env, self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake_inline(commands, data, self.elements, 'boxed')


class ArrayElement(AST):
    pointers = 0

    def __init__(self, array, index, other_indexes=None):
        super().__init__(CLASS, "array_element")

        self.array = array
        self.index = index
        self.other_indexes = other_indexes
        self.context = 'get'
        self.type = None
        self.children = [array, index, other_indexes]

    def interpret(self, env):
        return interpreter.array_element(env, self.array, self.index, self.other_indexes)

    def compile_vm(self, commands, data):
        return compile_vm.array_element(commands, data, self.array, self.index, self.other_indexes, self.context)


class ArrLen(AST):
    def __init__(self, args):
        super().__init__(CLASS, "arrlen")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.arr_len(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrlen(commands, data, self.args)


class UnboxedArrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "arrmake")

        self.args = args
        self.children = [args]
        self.type = 'unboxed'

    def interpret(self, env):
        return interpreter.unboxed_arr_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake(commands, data, self.args, 'unboxed')


class BoxedArrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "arrmake")

        self.args = args
        self.children = [args]
        self.type = 'boxed'

    def interpret(self, env):
        return interpreter.boxed_arr_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake(commands, data, self.args, 'boxed')
