from ..base import AST

CLASS = "declarations.object"


class Object(AST):
    def __init__(self, elements):
        super().__init__(CLASS, "object_def")

        self.elements = elements
        self.children = [elements]
