from zdiscord.util.error.ErrorFactory import SingletonException

class Singletone(object):
    __instance = None

    def __dispatch_object(cls):
        return object.__new__(cls)

    def __new__(cls, **kwargs):

        # Singleton gate
        if "kwargs" in kwargs.keys() and "polymorphic_evolution" in kwargs['kwargs'].keys() and "singleton" in kwargs['kwargs']['polymorphic_evolution']:
            if Singletone.__instance is None:
                Singletone.__instance = object.__new__(cls)
            return Singletone.__instance
        else:
            return object.__new__(cls)

    def ping_singleton(self):
        return Singletone.__instance is None

    def get_singleton(self):
        return Singletone.__instance