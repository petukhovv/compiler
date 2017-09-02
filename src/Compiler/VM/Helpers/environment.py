from pprint import pprint

class Environment:
    @staticmethod
    def create_label(env, name=None):
        label_number = env['label_counter']
        if name:
            env['labels_map'][name] = label_number
        env['label_counter'] += 1
        return label_number

    @staticmethod
    def create_var(env, name=None, type=None):
        var_number = env['var_counter']
        if name is not None:
            env['vars_map'][name] = {
                'number': var_number,
            }
            if type is not None:
                env['vars_map'][name]['type'] = type
        env['var_counter'] += 1
        return var_number

    @staticmethod
    def get_var_counter_value(env):
        return env['var_counter']

    @staticmethod
    def get_label(env, name):
        return env['labels_map'][name]

    @staticmethod
    def get_var(env, name, type=None):
        if type:
            env['vars_map'][name]['type'] = type
        return env['vars_map'][name]['number']

    @staticmethod
    def get_var_type(env, name):
        if 'type' in env['vars_map'][name]:
            return env['vars_map'][name]['type']
        else:
            return None

    @staticmethod
    def is_exist_var(env, name):
        return name in env['vars_map']
