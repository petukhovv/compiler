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

"""
'Reserved' used for parsing language expressions (keywords and operators = RESERVED-tokens).
It checks token tag and value.
"""
class Reserved(Combinator):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
           tokens[pos][0] == self.value and \
           tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None
