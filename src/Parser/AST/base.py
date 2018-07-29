import sys
import importlib


COMPILER_ASM_MODULE = "Compiler.ASM.Codegen"
COMPILER_VM_MODULE = "Compiler.VM.Codegen"
INTERPRETER_MODULE = "Interpreter.Eval"


class AST:
    def __init__(self, _class, _name):
        self._class = _class
        self._name = _name

    def compile_asm(self, compiler):
        module_name = "%s.%s" % (COMPILER_ASM_MODULE, self._class)

        if module_name not in sys.modules:
            importlib.import_module(module_name)

        return getattr(sys.modules[module_name], self._name)(compiler, self)

    def compile_vm(self, commands, data):
        module_name = "%s.%s" % (COMPILER_VM_MODULE, self._class)

        if module_name not in sys.modules:
            importlib.import_module(module_name)

        return getattr(sys.modules[module_name], self._name)(commands, data, self)

    def interpret(self, env):
        module_name = "%s.%s" % (INTERPRETER_MODULE, self._class)

        if module_name not in sys.modules:
            importlib.import_module(module_name)

        return getattr(sys.modules[module_name], self._name)(env, self)
