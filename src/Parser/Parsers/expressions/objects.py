from ...combinators import Lazy, Opt, Rep
from ...AST.expressions.objects import ObjectVal, ObjectMethod


def object_val():
    from ..common import id, keyword
    from .arithmetic import aexp

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
    deref_op_arr = keyword('[') + Lazy(aexp) + keyword(']')

    return id + deref_op_obj + Opt(Rep(deref_op_obj | deref_op_arr)) ^ process


def object_method():
    from ..common import id, keyword
    from .arguments import arguments

    def process(parsed):
        (((((object_name, _), method_name), _),  args), _) = parsed
        return ObjectMethod(object_name, method_name, args)
    return id + keyword('.') + id + keyword('(') + Opt(Lazy(arguments)) + keyword(')') ^ process
