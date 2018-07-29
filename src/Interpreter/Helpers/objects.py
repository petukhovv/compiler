class ObjectWrap:
    def __init__(self, env):
        self.env = env

    def get_var(self, name):
        return self.env['v'][name]

    def get_method(self, name):
        return self.env['f'][name]

    def set(self, name, value):
        self.env['v'][name] = value
