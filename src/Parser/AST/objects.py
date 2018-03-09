from .functions import Function

# from Compiler.VM import arrays as compile_vm
# from Compiler.ASM import arrays as compile_asm
from Interpreter import objects as interpreter


class Object:
    def __init__(self, elements):
        self.elements = elements
        self.children = [elements]

    def interpret(self, env):
        return interpreter.object_def(env, self.elements)

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectValDef:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = [name, value]

    def interpret(self, env):
        return interpreter.object_val_def(env, self.name, self.value)

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectMethodDef(Function):
    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectVal:
    def __init__(self, object_name, prop_name, other_prop_names):
        self.object_name = object_name
        self.prop_name = prop_name
        self.other_prop_names = other_prop_names

    def interpret(self, env):
        return interpreter.object_val(env, self.object_name, self.prop_name, self.other_prop_names)

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectMethod:
    def __init__(self, object_name, method_name, args):
        self.object_name = object_name
        self.method_name = method_name
        self.args = args

    def interpret(self, env):
        return interpreter.object_method(env, self.object_name, self.method_name, self.args)

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None

