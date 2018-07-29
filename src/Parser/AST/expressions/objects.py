from Parser.AST.base import AST

CLASS = "expressions.objects"


class ObjectVal(AST):
    def __init__(self, object_name, prop_name, other_prop_names):
        super().__init__(CLASS, "object_val")

        self.object_name = object_name
        self.prop_name = prop_name
        self.other_prop_names = other_prop_names
        self.context = None


class ObjectMethod(AST):
    def __init__(self, object_name, method_name, args):
        super().__init__(CLASS, "object_method")

        self.object_name = object_name
        self.method_name = method_name
        self.args = args
