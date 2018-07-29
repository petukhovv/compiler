# -*- coding: utf-8 -*-

ARGS_SEPARATOR = ' '

Push = 'PUSH'
Pop = 'POP'
Nop = 'NOP'
Dup = 'DUP'
Load = 'LOAD'
PLoad = 'PLOAD'
BLoad = 'BLOAD'
BPLoad = 'BPLOAD'
DLoad = 'DLOAD'
DBLoad = 'DBLOAD'
Store = 'STORE'
PStore = 'PSTORE'
BStore = 'BSTORE'
BPStore = 'BPSTORE'
DStore = 'DSTORE'
DBStore = 'DBSTORE'
Add = 'ADD'
Mul = 'MUL'
Sub = 'SUB'
Div = 'DIV'
Mod = 'MOD'
Invert = 'INVERT'
Compare = 'COMPARE'
Label = 'LABEL'
Jump = 'JUMP'
Jz = 'JZ'
Jnz = 'JNZ'
Read = 'READ'
Write = 'WRITE'
Enter = 'ENTER'
Call = 'CALL'
Function = 'FUNCTION'
Return = 'RETURN'
Malloc = 'MALLOC'
DMalloc = 'DMALLOC'
Log = 'LOG'


class Commands(list):
    def add(self, command, argument=None):
        """ Добалвение команды в список команд для стековой машины """
        self.append(self.gen(command, argument))
        return self

    @staticmethod
    def gen(command, argument=None):
        """ Генерация строкового представления заданной команды для стековой машины """
        argument = '' if argument is None else ARGS_SEPARATOR + str(argument)
        return command + argument

    def push_value(self, value, value_type):
        """ Генерация строкового представления заданной команды для стековой машины """
        self.add(Push, value)
        self.add(Push, value_type)

    def pop_value(self):
        """ Генерация строкового представления заданной команды для стековой машины """
        self.add(Pop)
        self.add(Pop)

    def load_value(self, variable, only_value=False, is_parent_scope=False):
        """ Генерация строкового представления заданной команды для стековой машины """
        if not only_value:
            self.add(PLoad if is_parent_scope else Load, variable)
        self.add(PLoad if is_parent_scope else Load, variable + 1)

    def store_value(self, variable, type=None, type_variable=None, is_parent_scope=False):
        """ Генерация строкового представления заданной команды для стековой машины """
        if type is not None:
            self.add(Push, type)
        elif type_variable:
            self.add(PLoad if is_parent_scope else Load, type_variable)
        self.add(Push, variable)
        self.add(BPStore if is_parent_scope else BStore, 1)
        self.add(PStore if is_parent_scope else Store, variable)

    def bload_value(self, data, only_value=False):
        """ Генерация строкового представления заданной команды для стековой машины """
        variable = data.var()

        if not only_value:
            self.add(Dup)
            self.add(Store, variable)
            self.add(BLoad, 0)
            self.add(Load, variable)
        self.add(BLoad, 1)

    def bstore_value(self, data):
        """ Генерация строкового представления заданной команды для стековой машины """
        variable = data.var()

        self.add(Dup)
        self.add(Store, variable)
        self.add(BStore, 0)
        self.add(Load, variable)
        self.add(BStore, 1)

    def dbload_value(self, value_type, value=0):
        """ Генерация строкового представления заданной команды для стековой машины """
        self.add(DBLoad, value)
        self.add(Push, value_type)

    def compare(self, compare_type):
        """ Генерация строкового представления заданной команды для стековой машины """
        self.add(Compare, compare_type)
        self.add(Pop)

    def clean_type(self):
        self.add(Pop)

    def set_and_return_type(self, value_type):
        self.add(Push, value_type)

        return value_type

    def get_type(self, data):
        variable_type = data.var()
        self.add(Store, variable_type)
        return variable_type
