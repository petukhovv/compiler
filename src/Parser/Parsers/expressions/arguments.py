def arguments():
    """
    Parsing function arguments statement (call point).
    """
    from ..common import enumeration
    from ..expressions.arrays import arr_exp
    from ..expressions.arithmetic import aexp
    from ..expressions.objects import object_method, object_val
    from ..expressions.logical import bexp
    from ..expressions.strings import str_exp, char_exp
    from ..declarations.object import object_def

    return enumeration(alternative_args_parser=(object_def() | object_val() | object_method()
                                                | aexp() | bexp() | str_exp() | char_exp() | arr_exp()))
