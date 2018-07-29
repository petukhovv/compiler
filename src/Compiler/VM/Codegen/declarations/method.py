from .function import function
from copy import copy


def object_method_def(commands, data, node):
    new_node = copy(node)
    new_node.name = "o%s!%s" % (data.context_objects[-1], node.name)

    return function(commands, data, new_node)