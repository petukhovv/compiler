import os


def ast_print(ast, level=0):
    for _ in range(0, level):
        print(' ', end="")
    type = ast.__class__.__name__
    print(type)
    if hasattr(ast, 'children'):
        for child in ast.children:
            ast_print(child, level + 1)
