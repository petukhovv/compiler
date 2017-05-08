from src.Parser.Parsers.strings import *
from src.Parser.AST.arrays import *

array_predefined_functions = {
    'arrlen': ArrLen
    # 'Arrmake': BoxedArrMake,
    # 'arrmake': UnboxedArrMake
}

def arr_exp():
    def process(parsed):
        ((_, elements), _) = parsed
        return UnboxedArray(elements)
    return keyword('[') + \
        enumeration(alternative_args_parser=(num | str_exp() | char_exp() | boolean)) + \
        keyword(']') ^ process
