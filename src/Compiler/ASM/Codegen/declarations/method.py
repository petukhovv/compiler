from copy import copy

from .function import function as compile_function


def object_method_def(compiler, node):
    new_node = copy(node)
    new_node.name = "o%s!%s" % (compiler.environment.object_list[-1][0], node.name)

    return compile_function(compiler, new_node)
