class CustomMeta(type):
    @staticmethod
    def get_custom_name(cls_name, name):
        if not name.startswith("_"):
            return "custom_" + name

        if name == '_':
            return "_custom_"
        if name == "__":
            return "__custom_"

        if name.startswith("__") and name.endswith("__"):
            return name
        if name.startswith("__"):
            return "__custom_" + name[2:]

        # name[0] == '_' and name[1] != '_'
        return "_custom_" + name[1:]

    def __new__(mcs, cls_name, bases, attributes):
        new_attributes = {}
        for key, value in attributes.items():
            new_attributes[mcs.get_custom_name(cls_name, key)] = value

        cls = super().__new__(mcs, cls_name, bases, new_attributes)

        def custom_setattr(self, name, value):
            call_name = name
            if self.__dict__.get(name) is None:
                call_name = cls.get_custom_name(type(self).__name__, name)

            super(type(self), self).__setattr__(call_name, value)

        cls.__setattr__ = custom_setattr
        return cls
