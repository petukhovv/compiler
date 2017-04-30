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

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)

"""
'Reserved' used for parsing language expressions (keywords and operators = RESERVED-tokens).
It checks token tag and value.
"""
class Reserved(Combinator):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, position):
        if position < len(tokens) and \
           tokens[position][0] == self.value and \
           tokens[position][1] is self.tag:
            return Result(tokens[position][0], position + 1)
        else:
            return None

"""
'Tag' used for parsing tokens with a specific tag.
It checks token tag only.
"""
class Tag(Combinator):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, position):
        if position < len(tokens) and tokens[position][1] is self.tag:
            return Result(tokens[position][0], position + 1)
        else:
            return None

"""
'Concat' first applies the left parser, and then the right parser.
If both are successful (result != None), returns a pair (left and right parser);
if at least one is unsuccessful, it returns None.
"""
class Concat(Combinator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, position):
        left_result = self.left(tokens, position)
        if left_result:
            right_result = self.right(tokens, left_result.position)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.position)
        return None

"""
'Alternate' applies the left parser, if it succeeds, returns the result;
if not, returns the right parser.
"""
class Alternate(Combinator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, position):
        left_result = self.left(tokens, position)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, position)
            return right_result

"""
'Opt' applies the parser, if it succeeds, returns the result;
if not, returns the result with None-value.
"""
class Opt(Combinator):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result:
            return result
        else:
            return Result(None, position)

"""
'Rep' applies the parser until it returns a successful result.
"""
class Rep(Combinator):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, position):
        results = []
        result = self.parser(tokens, position)
        while result:
            results.append(result.value)
            position = result.position
            result = self.parser(tokens, position)
        return Result(results, position)

"""
'Process' applies a function to the result of the parser, if it is successful.
"""
class Process(Combinator):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result:
            result.value = self.function(result.value)
            return result

"""
'Lazy' applies the parser to the place of the call (lazy call).
"""
class Lazy(Combinator):
    def __init__(self, parser_function):
        self.parser = None
        self.parser_function = parser_function

    def __call__(self, tokens, position):
        if not self.parser:
            self.parser = self.parser_function()
        return self.parser(tokens, position)

"""
'Phrase' applies the parser and returns its result only if the parser has absorbed all the tokens.
"""
class Phrase(Combinator):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result and result.position == len(tokens):
            return result
        else:
            return None

"""
'Exp' is necessary to parse lists according to the input two parsers: for target elements and for separators.
"""
class Exp(Combinator):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)
        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.position)
            if next_result:
                result = next_result
        return result
