from ...AST.statements.write import WriteStatement


def write_stmt():
    """ Parsing 'write' statement. """
    from ..common import keyword
    from ..expressions import objects, arithmetic

    def process(parsed):
        (((_, _), name), _) = parsed
        return WriteStatement(name)
    return keyword('write') + \
        keyword('(') + (objects.object_method() | objects.object_val() | arithmetic.aexp()) + keyword(')') ^ process
