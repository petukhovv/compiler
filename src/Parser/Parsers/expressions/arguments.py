def arguments():
    """
    Parsing function arguments statement (call point).
    """
    from ..common import enumeration
    from ..declarations import object
    from ..expressions import arrays, arithmetic, objects, logical, strings

    return enumeration(alternative_args_parser=(object.object_def() | objects.object_val() | objects.object_method()
                                                | arithmetic.aexp() | logical.bexp() | strings.str_exp() | strings.char_exp() | arrays.arr_exp()))
