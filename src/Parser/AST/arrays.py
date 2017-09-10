from src.Parser.AST.arithmetic_exprs import *

from src.Compiler.VM import arrays as compile_vm
from src.Interpreter import arrays as interpreter

class UnboxedArray:
    pointers = 0

    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return interpreter.unboxed_array(env, self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.unboxed(commands, data, self.elements)

class BoxedArray:
    pointers = 0

    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return interpreter.boxed_array(env, self.elements)

class ArrayElement:
    pointers = 0

    def __init__(self, array, index, other_indexes=None):
        self.array = array
        self.index = index
        self.other_indexes = other_indexes
        self.context = 'get'

    def eval(self, env):
        return interpreter.array_element(env, self.array, self.index, self.other_indexes)

    def compile_vm(self, commands, data):
        return compile_vm.array_element(commands, data, self.array, self.index, self.other_indexes, self.context)

class ArrLen:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.arr_len(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrlen(commands, data, self.args)

class UnboxedArrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.unboxed_arr_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.unboxed_arrmake(commands, data, self.args)

class BoxedArrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.boxed_arr_make(env, self.args)
