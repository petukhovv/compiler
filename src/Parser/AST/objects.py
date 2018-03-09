from .functions import Function


class Object:
    def __init__(self, elements):
        self.children = [elements]

    def interpret(self, env):
        return None

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectValDef:
    def __init__(self, name, value):
        self.children = [name, value]

    def interpret(self, env):
        return None

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectMethodDef(Function):
    def interpret(self, env):
        return None

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectVal:
    def __init__(self, object_name, prop_name):
        self.object_name = object_name
        self.prop_name = prop_name

    def interpret(self, env):
        return None

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
        return None

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None

