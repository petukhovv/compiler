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


class ObjectVal:
    def __init__(self, name, value):
        self.children = [name, value]

    def interpret(self, env):
        return None

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None


class ObjectMethod(Function):
    def interpret(self, env):
        return None

    def compile_vm(self, commands, data):
        return None

    def compile_asm(self, compiler):
        return None

