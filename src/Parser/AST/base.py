import sys


COMPILER_ASM_MODULE = "Compiler.ASM.Codegen"
COMPILER_VM_MODULE = "Compiler.VM.Codegen"
INTERPRETER_MODULE = "Interpreter.Eval"


class AST:
    def __init__(self, _class, _name):
        self._class = _class
        self._name = _name

    def compile_asm(self, compiler):
        module = sys.modules["%s.%s" % (COMPILER_ASM_MODULE, self._class)]

        return getattr(module, self._name)(compiler, self)

    def compile_vm(self, commands, data):
        module = sys.modules["%s.%s" % (COMPILER_VM_MODULE, self._class)]

        return getattr(module, self._name)(commands, data, self)

    def interpret(self, env):
        module = sys.modules["%s.%s" % (INTERPRETER_MODULE, self._class)]

        return getattr(module, self._name)(env, self)
