from ...Helpers.types import Types


def object_val_def(commands, data, node):
    prop_var = data.get_var(node.name.name, object_namespace=data.context_objects[-1])
    node.value.compile_vm(commands, data)
    commands.store_value(prop_var, type=Types.DYNAMIC)
