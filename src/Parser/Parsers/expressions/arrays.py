from ...combinators import Opt, Rep, Lazy
from ...AST.expressions.arrays import ArrLen, BoxedArrMake, UnboxedArrMake, UnboxedArray, BoxedArray, ArrayElement


array_predefined_functions = {
    'arrlen': ArrLen,
    'Arrmake': BoxedArrMake,
    'arrmake': UnboxedArrMake
}


def arr_exp():
    from ..common import id, boolean, num, enumeration
    from .strings import str_exp, char_exp

    elements = enumeration(alternative_args_parser=(num | str_exp() | char_exp() | boolean | id))
    return arr_unboxed_exp(elements) | arr_boxed_exp(elements)


def arr_unboxed_exp(elements):
    from ..common import keyword

    def process(parsed):
        ((_, elements), _) = parsed
        return UnboxedArray(elements)
    return keyword('[') + elements + keyword(']') ^ process


def arr_boxed_exp(elements):
    from ..common import keyword

    def process(parsed):
        ((_, elements), _) = parsed
        return BoxedArray(elements)
    return keyword('{') + elements + keyword('}') ^ process


def el_exp():
    from ..common import keyword, id
    from .arithmetic import aexp

    def process(parsed):
        ((name, ((_, index), _)), other_indexes_parsed) = parsed
        other_indexes = None
        if len(other_indexes_parsed) != 0:
            other_indexes = []
            for other_index_parsed in other_indexes_parsed:
                ((_, other_index), _) = other_index_parsed
                other_indexes.append(other_index)
        return ArrayElement(name, index, other_indexes)
    deref_op_obj = keyword('.') + id
    deref_op_arr = keyword('[') + Lazy(aexp) + keyword(']')
    return id + deref_op_arr + Opt(Rep(deref_op_arr | deref_op_obj)) ^ process
