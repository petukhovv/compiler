from ...AST.declarations.property import ObjectValDef
from ...AST.expressions.arithmetic import VarAexp


def object_val_def():
    from ..common import keyword, id
    from ..expressions import read, strings, arrays, arithmetic, logical

    def process(parsed):
        (((_, name), _), value) = parsed
        return ObjectValDef(name, value)
    return keyword('val') + (id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (logical.bexp(allow_single=True) | arithmetic.aexp() | logical.bexp() | read.read_stmt() | strings.str_exp() | strings.char_exp() | arrays.arr_exp()) ^ process
