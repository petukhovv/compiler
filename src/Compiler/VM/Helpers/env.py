from pprint import pprint

class Env:
    @staticmethod
    def label(env, name=None):
        label_number = env['label_counter']
        if name:
            env['labels'][name] = label_number
        env['label_counter'] += 1
        return label_number

    @staticmethod
    def var(env, name=None):
        var_number = env['var_counter']
        if Env.is_exist_var(env, name):
            return Env.get_var(env, name)
        if name is not None:
            env['vars'][name] = {
                'number': var_number,
            }
            if type is not None:
                env['vars'][name]['type'] = type
        env['var_counter'] += 1
        return var_number

    @staticmethod
    def get_label(env, name):
        return env['labels'][name]

    @staticmethod
    def get_var(env, name):
        if type:
            env['vars'][name]['type'] = type
        return env['vars'][name]['number']

    @staticmethod
    def is_exist_var(env, name):
        return name in env['vars']
