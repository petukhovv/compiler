from ...combinators import Opt, Lazy
from ...AST.declarations.method import ObjectMethodDef


def object_method_def():
    from ..common import id, keyword, enumeration
    from ..statements.base import stmt_list

    def process(parsed):
        (((((((_, name), _), args), _), _), body), _) = parsed
        return ObjectMethodDef(name, args, body)
    return keyword('fun') + id + \
        keyword('(') + Opt(enumeration()) + keyword(')') + \
        keyword('begin') + Opt(Lazy(stmt_list)) + \
        keyword('end') ^ process
