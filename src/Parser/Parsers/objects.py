from ..AST.objects import *

from .statements import *
from .basic import *
from .functions import *
from .boolean_exprs import *
from .io import *


def object_def():
    def process(parsed):
        ((_, elements), _) = parsed
        return Object(elements)
    return keyword('{') + enumeration(alternative_args_parser=object_val_def() | object_method_def()) + keyword('}') ^ process


def object_val_def():
    def process(parsed):
        (((_, name), _), value) = parsed
        return ObjectValDef(name, value)
    return keyword('val') + (id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (bexp(allow_single=True) | aexp() | bexp() | read_stmt() | str_exp() | char_exp() | arr_exp()) ^ process


def object_method_def():
    def process(parsed):
        (((((((_, name), _), args), _), _), body), _) = parsed
        return ObjectMethodDef(name, args, body)
    return keyword('fun') + id + \
        keyword('(') + Opt(enumeration()) + keyword(')') + \
        keyword('begin') + Opt(Lazy(statements.stmt_list)) + \
        keyword('end') ^ process


def object_val():
    def process(parsed):
        ((object_name, (_, prop_name)), other_prop_names) = parsed

        other_props = None
        if len(other_prop_names) != 0:
            other_props = []
            for other_prop_name in other_prop_names:
                if isinstance(other_prop_name[0], tuple):
                    ((_, other_prop), _) = other_prop_name
                else:
                    (_, other_prop) = other_prop_name
                other_props.append(other_prop)

        return ObjectVal(object_name, prop_name, other_props)

    deref_op_obj = keyword('.') + id
    deref_op_arr = keyword('[') + Lazy(arithmetic_exprs.aexp) + keyword(']')

    return (id | el_exp()) + deref_op_obj + Opt(Rep(deref_op_obj | deref_op_arr)) ^ process


def object_method():
    def process(parsed):
        (((((object_name, _), method_name), _),  args), _) = parsed
        return ObjectMethod(object_name, method_name, args)
    return id + keyword('.') + id + keyword('(') + Opt(Lazy(args_call)) + keyword(')') ^ process
