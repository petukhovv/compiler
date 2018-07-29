from ...Helpers.commands import Write


def write_statement(commands, data, node):
    node.aexp.compile_vm(commands, data)
    commands.clean_type()
    commands.add(Write)
