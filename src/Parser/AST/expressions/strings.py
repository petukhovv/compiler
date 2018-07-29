from Compiler.ASM.Codegen.expressions import strings as compile_asm
from Compiler.VM.Codegen.expressions import strings as compile_vm
from Interpreter.Eval.expressions import strings as interpreter

from Parser.AST.base import AST

CLASS = "expressions.strings"


class Char(AST):
    def __init__(self, character):
        super().__init__(CLASS, "char")

        self.character = character


class String(AST):
    def __init__(self, characters):
        super().__init__(CLASS, "string")

        self.characters = characters


class StrLen(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strlen")

        self.args = args
        self.children = [args]


class StrGet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strget")

        self.args = args
        self.children = [args]


class StrSub(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strsub")

        self.args = args
        self.children = [args]


class StrDup(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strdup")

        self.args = args
        self.children = [args]


class StrCat(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strcat")

        self.args = args
        self.children = [args]


class StrCmp(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strcmp")

        self.args = args
        self.children = [args]


class StrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strmake")

        self.args = args
        self.children = [args]
