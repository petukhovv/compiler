from ..Core.types import Types
from ..Core.commands import Commands
from ..Core.registers import Registers
from ..Runtime.atoi import *


class GC(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if GC.is_loaded:
            return

        self.load('gc.asm', ['gc_decrease', 'gc_increase', 'gc_clean', 'gc_start_if_need'])
        GC.is_loaded = True

    def run(self):
        self.compiler.code.add(Commands.CALL, ['gc_decrease'])

    def clean(self):
        self.compiler.code.add(Commands.CALL, ['gc_clean'])

    def increment(self):
        self.compiler.code.add(Commands.CALL, ['gc_increase'])

    def check_args(self, args):
        for arg in args:
            var_pointer = self.compiler.environment.get_arg(arg)
            var_type_pointer = self.compiler.environment.get_arg_runtime_type(arg)
            self.compiler.code.add(Commands.MOV, [Registers.EAX, var_pointer])
            self.compiler.code.add(Commands.MOV, [Registers.EBX, var_type_pointer])
            self.compiler.code.add(Commands.CALL, ['gc_start_if_need'])

    def check_local_vars(self):
        for variable in self.compiler.environment.get_all_vars():
            var_name = self.compiler.environment.get_local_var(variable)
            var_type = self.compiler.environment.get_local_var_type(variable)
            if var_type == Types.BOXED_ARR or var_type == Types.UNBOXED_ARR:
                self.compiler.code.add(Commands.MOV, [Registers.EAX, var_name])
                self.run()
