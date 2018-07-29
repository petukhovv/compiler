from ...AST.statements.write import WriteStatement


def write_stmt():
    """ Parsing 'write' statement. """
    from ..common import keyword
    from ..expressions.objects import object_method, object_val
    from ..expressions.arithmetic import aexp

    def process(parsed):
        (((_, _), name), _) = parsed
        return WriteStatement(name)
    return keyword('write') + \
        keyword('(') + (object_method() | object_val() | aexp()) + keyword(')') ^ process
