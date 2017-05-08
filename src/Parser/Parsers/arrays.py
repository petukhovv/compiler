import sys

from src.Parser.Parsers.strings import *

from src.Parser.AST.arrays import *

arithmetic_exprs = sys.modules[__package__ + '.arithmetic_exprs']

array_predefined_functions = {
    'arrlen': ArrLen,
    # 'Arrmake': BoxedArrMake,
    'arrmake': UnboxedArrMake
}

def arr_exp():
    def process(parsed):
        ((_, elements), _) = parsed
        return UnboxedArray(elements)
    return keyword('[') + \
        enumeration(alternative_args_parser=(num | str_exp() | char_exp() | boolean)) + \
        keyword(']') ^ process

def el_exp():
    def process(parsed):
        (((name, _), index), _) = parsed
        return ArrayElement(name, index)
    return id + keyword('[') + Lazy(arithmetic_exprs.aexp) + keyword(']') ^ process
