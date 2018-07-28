from .functions import Function

from Compiler.VM import objects as compile_vm
from Compiler.ASM import objects as compile_asm
from Interpreter import objects as interpreter

from .base import AST

CLASS = "objects"


class Object(AST):
    def __init__(self, elements):
        super().__init__(CLASS, "object_def")

        self.elements = elements
        self.children = [elements]

    def interpret(self, env):
        return interpreter.object_def(env, self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.object_def(commands, data, self.elements)


class ObjectValDef(AST):
    def __init__(self, name, value):
        super().__init__(CLASS, "object_val_def")

        self.name = name
        self.value = value
        self.children = [name, value]

    def interpret(self, env):
        return interpreter.object_val_def(env, self.name, self.value)

    def compile_vm(self, commands, data):
        return compile_vm.object_val_def(commands, data, self.name, self.value)


class ObjectMethodDef(Function):
    def compile_vm(self, commands, data):
        return compile_vm.object_method_def(commands, data, self.name, self.args, self.body)


class ObjectVal(AST):
    def __init__(self, object_name, prop_name, other_prop_names):
        super().__init__(CLASS, "object_val")

        self.object_name = object_name
        self.prop_name = prop_name
        self.other_prop_names = other_prop_names
        self.context = None

    def interpret(self, env):
        return interpreter.object_val(env, self.object_name, self.prop_name, self.other_prop_names)

    def compile_vm(self, commands, data):
        return compile_vm.object_val(commands, data, self.object_name, self.prop_name, self.other_prop_names, self.context)


class ObjectMethod(AST):
    def __init__(self, object_name, method_name, args):
        super().__init__(CLASS, "object_method")

        self.object_name = object_name
        self.method_name = method_name
        self.args = args

    def interpret(self, env):
        return interpreter.object_method(env, self.object_name, self.method_name, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.object_method(commands, data, self.object_name, self.method_name, self.args)
