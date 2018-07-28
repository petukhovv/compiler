from ..Core.types import Types
from ..Core.commands import Commands
from ..Core.registers import Registers
from ..Runtime.atoi import *
from .free import Free


class GC(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if GC.is_loaded:
            return

        self.load('gc.asm', ['gc_decrement', 'gc_increment'])
        self.load('write_error.asm', ['write_error'])
        GC.is_loaded = True
        Free(compiler)

    def decrement(self):
        self.compiler.code.add(Commands.CALL, ['gc_decrement'])

    def increment(self):
        self.compiler.code.add(Commands.CALL, ['gc_increment'])

    def check_args(self, args):
        for arg in args:
            var_pointer = self.compiler.environment.get_arg(arg)
            var_type_pointer = self.compiler.environment.get_arg_runtime_type(arg)
            self.compiler.code.add(Commands.MOV, [Registers.EAX, var_pointer])
            self.compiler.code.add(Commands.MOV, [Registers.EBX, var_type_pointer])
            self.decrement()

    def check_local_vars(self):
        for variable in self.compiler.environment.get_all_vars():
            var_name = self.compiler.environment.get_local_var(variable)
            var_type = self.compiler.environment.get_local_var_runtime_type(variable)
            self.compiler.code.add(Commands.MOV, [Registers.EAX, var_name])
            self.compiler.code.add(Commands.MOV, [Registers.EBX, var_type])
            self.decrement()
