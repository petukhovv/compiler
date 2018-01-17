# -*- coding: utf-8 -*-


class Commands:
    def __init__(self, compiler):
        self.compiler = compiler

    def set_and_return_type(self, value_type):
        self.compiler.code.add('push', [value_type])

        return value_type

    def clean_type(self):
        self.compiler.code.add('add', ['esp', 4])
