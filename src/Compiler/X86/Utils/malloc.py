from .base import Base


def malloc(compiler):
    compiler.code.add('pop', ['eax'])
    compiler.code.add('push', ['ebp'])
    compiler.code.add('mov', ['ebp', 'esp'])
    compiler.code.add('sub', ['esp', 4])
    compiler.code.add('push', ['eax'])
    compiler.code.add('call', ['_malloc'])
    compiler.code.add('add', ['esp', 8])
    compiler.code.add('pop', ['ebp'])

