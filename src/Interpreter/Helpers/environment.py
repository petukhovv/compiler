from copy import deepcopy


class Environment:
    """
    Integer arithmetic expression class for AST.
    interpret - runtime function for Evaluator (just return i).
    Example: 54
    """
    def __init__(self, env=None):
        self.env = env

    def set(self, variable, value):
        env = self.env
        target_env = None
        while not target_env:
            if variable in env['v']:
                target_env = env
            elif env['p']:
                env = env['p']
            else:
                break
        if not target_env:
            target_env = self.env
        target_env['v'][variable] = value

        return None

    def get(self, variable):
        env = self.env
        while env:
            if variable in env['v']:
                return deepcopy(env['v'][variable])
            elif env['p']:
                env = env['p']
            else:
                env = None

        return None

    def create(self, func_env=None):
        env = {
            'v': {},
            'f': {},
            'r': None,
            'p': self.env
        }
        if func_env:
            env['f'] = func_env

        return env
