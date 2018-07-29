from ...AST.declarations.property import ObjectValDef
from ...AST.expressions.arithmetic import VarAexp


def object_val_def():
    from ..common import keyword, id
    from ..expressions.read import read_stmt
    from ..expressions.strings import str_exp, char_exp
    from ..expressions.arrays import arr_exp
    from ..expressions.arithmetic import aexp
    from ..expressions.logical import bexp

    def process(parsed):
        (((_, name), _), value) = parsed
        return ObjectValDef(name, value)
    return keyword('val') + (id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (bexp(allow_single=True) | aexp() | bexp() | read_stmt() | str_exp() | char_exp() | arr_exp()) ^ process
