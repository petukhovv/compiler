from src.Parser.Parsers.functions import *
from src.Parser.Parsers.io import *
from src.Parser.Parsers.arrays import *

from src.Parser.AST.statements import *

"""
Parsing simple assign statement.
Example: x := 56
"""
def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return (el_exp() | id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (bexp() | aexp() | read_stmt() | str_exp() | char_exp() | arr_exp()) ^ process

"""
Parsing statement list (by ';' separator).
Example:
x := 56;
y := 12;
z := 512
"""
def stmt_list():
    def process_stmt(x):
        return lambda l, r: CompoundStatement(l, r)
    def process(parsed_list):
        if len(parsed_list) == 1:
            return parsed_list[0]
        return reduce(lambda stmt1, stmt2: CompoundStatement(stmt1, stmt2), parsed_list)
    return Rep(fun() | Exp(stmt(), keyword(';') ^ process_stmt)) ^ process

"""
Parsing 'if' statement.
"""
def if_stmt():
    def process(parsed):
        ((((((_, condition), _), true_stmt), alternatives_stmt_parsed), false_stmt_parsed), _) = parsed
        if false_stmt_parsed:
            (_, false_stmt) = false_stmt_parsed
        else:
            false_stmt = None
        if alternatives_stmt_parsed:
            alternatives_stmt = []
            for alternative_stmt_parsed in alternatives_stmt_parsed:
                (((_, alternative_condition), _), alternative_body) = alternative_stmt_parsed
                alternatives_stmt.append(IfStatement(alternative_condition, alternative_body, None))
        else:
            alternatives_stmt = None
        return IfStatement(condition, true_stmt, alternatives_stmt, false_stmt)
    return keyword('if') + bexp(allow_single=True) + keyword('then') + Lazy(stmt_list) + \
           Opt(Rep(keyword('elif') + bexp(allow_single=True) + keyword('then') + Lazy(stmt_list))) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('fi') ^ process

"""
Parsing 'while' statement.
"""
def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp(allow_single=True) + \
        keyword('do') + Lazy(stmt_list) + \
        keyword('od') ^ process

"""
Parsing 'for' statement.
"""
def for_stmt():
    def process(parsed):
        ((((((((_, stmt1), _), stmt2), _), stmt3), _), body), _) = parsed
        return ForStatement(stmt1, stmt2, stmt3, body)
    return keyword('for') + (assign_stmt() | skip_stmt()) + keyword(',') + \
        bexp(allow_single=True) + keyword(',') + \
        assign_stmt() + keyword('do') + \
        Lazy(stmt_list) + keyword('od') ^ process

"""
Parsing 'repeat' statement.
"""
def repeat_stmt():
    def process(parsed):
        (((_, body), _), condition) = parsed
        return RepeatStatement(condition, body)
    return keyword('repeat') + Lazy(stmt_list) + \
        keyword('until') + bexp(allow_single=True) ^ process

"""
Parsing 'skip' statement.
"""
def skip_stmt():
    return keyword('skip') ^ (lambda parsed: SkipStatement())

"""
Main statement parser.
Try to first parse as 'assign' statement,
if not possible - as 'if' statement,
if not possible - as 'while' statement.
"""
def stmt():
    return assign_stmt() | \
        if_stmt() | \
        while_stmt() | \
        repeat_stmt() | \
        for_stmt() | \
        return_stmt() | \
        write_stmt() | \
        fun_call_stmt() | \
        skip_stmt()
