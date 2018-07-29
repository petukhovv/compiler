from ...Runtime.write import Write


def write_statement(compiler, node):
    value_type = node.aexp.compile_asm(compiler)
    compiler.types.pop()
    Write(compiler).call(value_type)
