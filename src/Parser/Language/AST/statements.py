from equality import *

"""
Base class for statement classes.
"""
class Statement(Equality):
    pass

"""
Assign statement class for AST.
Example: x := 56
"""
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)
