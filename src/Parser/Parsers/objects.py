from ..AST.objects import *

from .statements import *
from .basic import *
from .boolean_exprs import *
from .io import *


def object_def():
    def process(parsed):
        ((_, elements), _) = parsed
        return Object(elements)
    return keyword('{') + enumeration(alternative_args_parser=object_val() | object_method()) + keyword('}') ^ process


def object_val():
    def process(parsed):
        (((_, name), _), value) = parsed
        return ObjectVal(name, value)
    return keyword('val') + (id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (bexp(allow_single=True) | aexp() | bexp() | read_stmt() | str_exp() | char_exp() | arr_exp()) ^ process


def object_method():
    def process(parsed):
        (((((((_, name), _), args), _), _), body), _) = parsed
        return ObjectMethod(name, args, body)
    return keyword('method') + id + \
        keyword('(') + Opt(enumeration()) + keyword(')') + \
        keyword('begin') + Opt(Lazy(statements.stmt_list)) + \
        keyword('end') ^ process
