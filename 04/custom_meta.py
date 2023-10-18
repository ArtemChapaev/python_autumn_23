class CustomMeta(type):
    @staticmethod
    def get_custom_name(name):
        if len(name) > 4 and name.startswith("__") and name.endswith("__"):
            return name

        return "custom_" + name

    def __new__(mcs, cls_name, bases, attributes):
        new_attributes = {}
        for key, value in attributes.items():
            new_attributes[mcs.get_custom_name(key)] = value

        cls = super().__new__(mcs, cls_name, bases, new_attributes)

        def custom_setattr(self, name, value):
            call_name = name
            if self.__dict__.get(name) is None:
                call_name = cls.get_custom_name(name)

            super(type(self), self).__setattr__(call_name, value)

        cls.__setattr__ = custom_setattr
        return cls
