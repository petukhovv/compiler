from Parser.AST.arithmetic_exprs import *

from Compiler.VM import arrays as compile_vm
from Compiler.X86 import arrays as compile_x86
from Interpreter import arrays as interpreter


class UnboxedArray:
    pointers = 0

    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return interpreter.unboxed_array(env, self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake_inline(commands, data, self.elements, 'unboxed')

    def compile_x86(self, compiler):
        return compile_x86.arrmake_inline(compiler, self.elements, 'unboxed')


class BoxedArray:
    pointers = 0

    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return interpreter.boxed_array(env, self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake_inline(commands, data, self.elements, 'boxed')

    def compile_x86(self, compiler):
        return compile_x86.arrmake_inline(compiler, self.elements, 'boxed')


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

    def compile_x86(self, compiler):
        return compile_x86.array_element(compiler, self.array, self.index, self.other_indexes, self.context)


class ArrLen:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.arr_len(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrlen(commands, data, self.args)

    def compile_x86(self, compiler):
        return compile_x86.arrlen(compiler, self.args)


class UnboxedArrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.unboxed_arr_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake(commands, data, self.args, 'unboxed')

    def compile_x86(self, compiler):
        return compile_x86.arrmake(compiler, self.args, 'unboxed')


class BoxedArrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.boxed_arr_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.arrmake(commands, data, self.args, 'boxed')

    def compile_x86(self, compiler):
        return compile_x86.arrmake(compiler, self.args, 'boxed')
