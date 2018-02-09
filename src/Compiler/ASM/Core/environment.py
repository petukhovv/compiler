from .types import Types


class Environment:
    counter = 0         # Function counter
    var_counter = 0         # Function counter
    list = {            # Function list
        'root': {
            'memory': 0,
            'vars': {}
        }
    }
    current = None      # The name of the function in which we are currently

    def set_return_type(self, type):
        if self.current is None:
            return

        self.list[self.current]['return_type'] = type

    def get_return_type(self, name):
        return self.list[name]['return_type']

    def set_args(self, args):
        if self.current is None:
            return

        self.list[self.current]['args'] = args

    def get_args(self, name=None):
        if name is None:
            name = self.current

        return self.list[name]['args'] if name in self.list else None

    def start(self, name):
        self.counter += 1
        self.list[name] = {
            'memory': 0,
            'vars': {},
            'args': None,
            'return_type': Types.NOTHING,
            'number': self.counter
        }
        self.current = name

        return self.counter

    def finish(self):
        need_memory = self.list[self.current]['memory']
        self.current = None

        return need_memory

    def get_number(self, name):
        return self.list[name]['number'] if name in self.list else None

    def add_local_var(self, type=None, name=None, size=None):
        env = self.list[self.current if self.current else 'root']

        if name is None:
            name = 'var_%s' % self.var_counter
            self.var_counter += 1

        if name in env['vars']:
            return self.get_local_var(name, as_object=type is None)

        stack_pointer = env['memory']
        size = Types.SIZES[type] if type else size + 4
        env['vars'][name] = {
            'stack_pointer': stack_pointer,
            'size': size,
            'type': type
        }
        env['memory'] += size

        return self.get_local_var(name, as_object=type is None)

    def get_local_var(self, name=None, as_object=False):
        env = self.list[self.current if self.current else 'root']
        if name in env['vars']:
            size = env['vars'][name]['size']
            type = env['vars'][name]['type']
            stack_pointer = env['vars'][name]['stack_pointer']
            if as_object:
                var_pointer = {'pointer': 'ebp', 'offset': stack_pointer}
            elif type:
                var_pointer = '%s [ebp-%s]' % (Types.ASM[size], stack_pointer + 4)
            else:
                var_pointer = '%s [ebp-%s]' % (Types.ASM[4], stack_pointer + 4)
        else:
            var_pointer = '%s [ebp+%s]' % (Types.ASM[4], (env['args'][name] + 2) * 4)\
                if name in env['args'] else None

        return var_pointer

    def get_local_var_type(self, name=None):
        env = self.list[self.current if self.current else 'root']

        return env['vars'][name]['type'] if name in env['vars'] else Types.INT

    def is_exist_local_var(self, name=None):
        env = self.list[self.current if self.current else 'root']

        return name in env['vars']
