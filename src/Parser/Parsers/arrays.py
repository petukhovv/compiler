import sys

from src.Parser.Parsers.strings import *

from src.Parser.AST.arrays import *

arithmetic_exprs = sys.modules[__package__ + '.arithmetic_exprs']

array_predefined_functions = {
    'arrlen': ArrLen,
    'Arrmake': BoxedArrMake,
    'arrmake': UnboxedArrMake
}

def arr_exp():
    elements = enumeration(alternative_args_parser=(num | str_exp() | char_exp() | boolean))
    return arr_unboxed_exp(elements) | arr_boxed_exp(elements)

def arr_unboxed_exp(elements):
    def process(parsed):
        ((_, elements), _) = parsed
        return UnboxedArray(elements)
    return keyword('[') + elements + keyword(']') ^ process

def arr_boxed_exp(elements):
    def process(parsed):
        ((_, elements), _) = parsed
        return BoxedArray(elements)
    return keyword('{') + elements + keyword('}') ^ process

def el_exp():
    def process(parsed):
        ((name, ((_, index), _)), other_indexes_parsed) = parsed
        other_indexes = None
        if len(other_indexes_parsed) != 0:
            other_indexes = []
            for other_index_parsed in other_indexes_parsed:
                ((_, other_index), _) = other_index_parsed
                other_indexes.append(other_index)
        return ArrayElement(name, index, other_indexes)
    deref_op = keyword('[') + Lazy(arithmetic_exprs.aexp) + keyword(']')
    return id + deref_op + Opt(Rep(deref_op)) ^ process
