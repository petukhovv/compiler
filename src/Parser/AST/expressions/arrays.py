from Compiler.VM.Codegen.expressions import arrays as compile_vm
from Compiler.ASM.Codegen.expressions import arrays as compile_asm
from Interpreter.Eval.expressions import arrays as interpreter

from Parser.AST.base import AST

CLASS = "expressions.arrays"


class UnboxedArray(AST):
    pointers = 0

    def __init__(self, elements):
        super().__init__(CLASS, "arrmake_inline")

        self.elements = elements
        self.children = [elements]
        self.type = 'unboxed'


class BoxedArray(AST):
    pointers = 0

    def __init__(self, elements):
        super().__init__(CLASS, "arrmake_inline")

        self.elements = elements
        self.children = [elements]
        self.type = 'boxed'


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


class ArrLen(AST):
    def __init__(self, args):
        super().__init__(CLASS, "arrlen")

        self.args = args
        self.children = [args]


class UnboxedArrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "arrmake")

        self.args = args
        self.children = [args]
        self.type = 'unboxed'


class BoxedArrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "arrmake")

        self.args = args
        self.children = [args]
        self.type = 'boxed'

