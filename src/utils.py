class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in Singleton.instances:
            return Singleton.instances[cls]
        else:
            new_instance = super(Singleton, cls).__call__(*args, **kwargs)
            Singleton.instances[cls] = new_instance
            return new_instance

