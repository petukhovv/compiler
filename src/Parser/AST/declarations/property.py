from ..base import AST

CLASS = "declarations.property"


class ObjectValDef(AST):
    def __init__(self, name, value):
        super().__init__(CLASS, "object_val_def")

        self.name = name
        self.value = value
        self.children = [name, value]