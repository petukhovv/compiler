"""
Object of this class will be returned by parsers.
    Value - intermediate result, part of AST.
    Position - next token position.
"""
class Result:
    def __init__(self, value, position):
        self.value = value
        self.position = position

"""
Base class for combinators.
__call__ will override by subclasses.
"""
class Combinator:
    def __call__(self, tokens, position):
        return None
