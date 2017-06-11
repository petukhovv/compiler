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
    def create_var(env, name):
        env['vars_map'][name] = env['var_counter']
        var_number = env['var_counter']
        env['var_counter'] += 1
        return var_number

    @staticmethod
    def get_label(env, name):
        return env['labels_map'][name]

    @staticmethod
    def get_var(env, name):
        return env['vars_map'][name]

    @staticmethod
    def is_exist_var(env, name):
        return name in env['vars_map']
