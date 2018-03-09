from Compiler.ASM import statements as compile_asm
from Compiler.VM import statements as compile_vm
from Interpreter import statements as interpreter


class AssignStatement:
    """
    Assign statement class for AST.
    interpret - runtime function for Evaluator (return variable by name from environment).
    Example: x := 56
    """
    def __init__(self, variable, aexp):
        self.variable = variable
        self.aexp = aexp
        self.children = [variable, aexp]

    def interpret(self, env):
        return interpreter.assign_statement(env, self.variable, self.aexp)

    def compile_vm(self, commands, data):
        return compile_vm.assign_statement(commands, data, self.variable, self.aexp)

    def compile_asm(self, compiler):
        return compile_asm.assign_statement(compiler, self.variable, self.aexp)


class CompoundStatement:
    """
    Compound statement class for AST.
    interpret - runtime function for Evaluator (interpret first and second statement operators).
    """
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.children = [first, second]

    def interpret(self, env):
        return interpreter.compound_statement(env, self.first, self.second)

    def compile_vm(self, commands, data):
        return compile_vm.compound_statement(commands, data, self.first, self.second)

    def compile_asm(self, compiler):
        return compile_asm.compound_statement(compiler, self.first, self.second)


class IfStatement:
    """
    'If' statement class for AST.
    interpret - runtime function for Evaluator (true of false statement depending on condition).
    """
    def __init__(self, condition, true_stmt, alternatives_stmt=None, false_stmt=None):
        self.condition = condition
        self.true_stmt = true_stmt
        self.alternatives_stmt = alternatives_stmt
        self.false_stmt = false_stmt
        self.children = [condition, true_stmt, alternatives_stmt, false_stmt]

    def interpret(self, env):
        return interpreter.if_statement(env, self.condition, self.true_stmt, self.alternatives_stmt, self.false_stmt)

    def compile_vm(self, commands, data, label_endif=None):
        return compile_vm.if_statement(commands, data, self.condition, self.true_stmt, self.alternatives_stmt, self.false_stmt, label_endif)

    def compile_asm(self, compiler, label_endif=None):
        return compile_asm.if_statement(compiler, self.condition, self.true_stmt, self.alternatives_stmt, self.false_stmt, label_endif)


class WhileStatement:
    """
    'While' statement class for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.children = [body, condition]

    def interpret(self, env):
        return interpreter.while_statement(env, self.condition, self.body)

    def compile_vm(self, commands, data):
        return compile_vm.while_statement(commands, data, self.condition, self.body)

    def compile_asm(self, compiler):
        return compile_asm.while_statement(compiler, self.condition, self.body)


class ForStatement:
    """
    'For' statement class for AST.
    interpret - runtime function for Evaluator ('for' loop).
    """
    def __init__(self, stmt1, stmt2, stmt3, body):
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.stmt3 = stmt3
        self.body = body
        self.children = [stmt1, stmt2, stmt3, body]

    def interpret(self, env):
        return interpreter.for_statement(env, self.stmt1, self.stmt2, self.stmt3, self.body)

    def compile_vm(self, commands, data):
        return compile_vm.for_statement(commands, data, self.stmt1, self.stmt2, self.stmt3, self.body)

    def compile_asm(self, compiler):
        return compile_asm.for_statement(compiler, self.stmt1, self.stmt2, self.stmt3, self.body)


class RepeatStatement:
    """
    'Repeat' statement class for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.children = [condition, body]

    def interpret(self, env):
        return interpreter.repeat_statement(env, self.condition, self.body)

    def compile_vm(self, commands, data):
        return compile_vm.repeat_statement(commands, data, self.condition, self.body)

    def compile_asm(self, compiler):
        return compile_asm.repeat_statement(compiler, self.condition, self.body)


class SkipStatement:
    """
    'Skip' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def interpret(self, env):
        return interpreter.skip_statement(env)

    def compile_vm(self, commands, data):
        return compile_vm.skip_statement(commands, data)

    def compile_asm(self, compiler):
        return compile_asm.skip_statement(compiler)
