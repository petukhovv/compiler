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
    return keyword('method') + id + \
        keyword('(') + Opt(enumeration()) + keyword(')') + \
        keyword('begin') + Opt(Lazy(statements.stmt_list)) + \
        keyword('end') ^ process


def object_val():
    def process(parsed):
        ((object_name, _), prop_name) = parsed
        return ObjectVal(object_name, prop_name)
    return id + keyword('.') + id ^ process


def object_method():
    def process(parsed):
        (((((object_name, _), method_name), _),  args), _) = parsed
        return ObjectMethod(object_name, method_name, args)
    return id + keyword('.') + id + keyword('(') + Opt(Lazy(args_call)) + keyword(')') ^ process
