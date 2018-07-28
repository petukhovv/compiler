import sys


COMPILER_ASM_MODULE = "Compiler.ASM"


class AST:
    def __init__(self, _class, _name):
        self._class = _class
        self._name = _name

    def compile_asm(self, compiler):
        module = sys.modules["%s.%s" % (COMPILER_ASM_MODULE, self._class)]

        return getattr(module, self._name)(compiler, self)
