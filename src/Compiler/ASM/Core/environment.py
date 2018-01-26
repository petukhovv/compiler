class Environment:
    counter = 0         # Function counter
    list = {}           # Function list
    current = None      # The name of the function in which we are currently

    def set_return_type(self, type):
        if self.current is None:
            return

        self.list[self.current]['return_type'] = type

    def get_return_type(self, name):
        return self.list[name]['return_type'] if name in self.list else None

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
            'args': None,
            'return_type': None,
            'number': self.counter
        }
        self.current = name

        return self.counter

    def finish(self):
        self.current = None

    def get_number(self, name):
        return self.list[name]['number'] if name in self.list else None
