from pprint import pprint

class Environment:
    @staticmethod
    def get_current_env(data):
        env_count = len(data.environments)
        if env_count == 0:
            return data
        return data.environments[env_count - 1]

    @staticmethod
    def get_env(data, env_number):
        env_count = len(data.environments)
        if env_count < env_number:
            return None
        if env_count == env_number:
            return data
        return data.environments[env_count - env_number - 1]

    @staticmethod
    def store_variable(data, name, value):
        data = Environment.get_current_env(data)
        data.stack[name] = value

    @staticmethod
    def store_dynamic_variable(data, name, value):
        data = Environment.get_current_env(data)
        data.heap[name] = value

    @staticmethod
    def search_variable(data, variable):
        data = Environment.get_current_env(data)

        if variable in data.stack:
            return data.stack[variable]
        else:
            return None

    @staticmethod
    def search_heap_variable(data, variable):
        data = Environment.get_current_env(data)
        if variable in data.heap:
            return data.heap[variable]
        else:
            return None

    @staticmethod
    def create(data):
        class new_environment:
            stack = {}
            heap = []
        data.environments.append(new_environment)

        return new_environment

    @staticmethod
    def clear(data):
        data.environments.pop()
