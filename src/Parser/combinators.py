"""
Object of this class will be returned by parsers.
    Value - intermediate result, part of AST.
    Position - next token position.
"""
class Result:
    def __init__(self, value, position):
        self.value = value
        self.position = position
