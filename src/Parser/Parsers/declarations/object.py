from ...AST.declarations.object import Object


def object_def():
    from ..declarations import method, property
    from ..common import keyword, enumeration

    def process(parsed):
        ((_, elements), _) = parsed
        return Object(elements)
    return keyword('{') + enumeration(alternative_args_parser=property.object_val_def() | method.object_method_def()) + keyword('}') ^ process
