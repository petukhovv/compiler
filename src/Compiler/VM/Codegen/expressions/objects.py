from ...Helpers.types import Types
from .call import call_statement
from copy import copy


def object_val(commands, data, node):
    if node.object_name == 'this':
        obj_var = data.context_objects[-1]
    else:
        obj_var = data.get_object_name(data.get_var(node.object_name, is_root=True))

    prop_var = data.get_object_property(obj_var, node.prop_name, Types.DYNAMIC)

    if node.context == 'assign':
        commands.store_value(prop_var, type=Types.DYNAMIC, is_parent_scope=len(data.context_objects) > 0)
    else:
        commands.load_value(prop_var, is_parent_scope=len(data.context_objects) > 0)

    return Types.DYNAMIC


def object_method(commands, data, node):
    if node.object_name == 'this':
        obj_var = data.context_objects[-1]
    else:
        obj_var = data.get_object_name(data.get_var(node.object_name, is_root=True))

    new_node = copy(node)
    new_node.name = "o%s!%s" % (obj_var, node.method_name)

    return call_statement(commands, data, new_node)
