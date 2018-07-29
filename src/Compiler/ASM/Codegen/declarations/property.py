from ...Core.commands import Commands


def object_val_def(compiler, node):
    value_type = node.value.compile_asm(compiler)

    prop_var = compiler.environment.add_local_var(value_type, node.name.name, object_namespace=compiler.environment.object_list[-1][0])
    compiler.code.add(Commands.POP, prop_var)
