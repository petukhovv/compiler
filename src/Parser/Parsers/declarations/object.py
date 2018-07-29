from ...AST.declarations.object import Object


def object_def():
    from .property import object_val_def
    from .method import object_method_def
    from ..common import keyword, enumeration

    def process(parsed):
        ((_, elements), _) = parsed
        return Object(elements)
    return keyword('{') + enumeration(alternative_args_parser=object_val_def() | object_method_def()) + keyword('}') ^ process
