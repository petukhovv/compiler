from Parser.AST.base import AST

CLASS = "statements.strings"


class StrSet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strset")

        self.args = args
        self.children = [args]
