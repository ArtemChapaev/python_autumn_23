import re


class RomanNumber:
    def __set_name__(self, owner, attr_name):
        self.name = f"roman_number_{attr_name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if not isinstance(val, str):
            raise ValueError("str required")

        if not re.search("^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", val):
            raise ValueError("roman number required")

        return setattr(obj, self.name, val)

    def __delete__(self, obj):
        return delattr(obj, self.name)


class CelsiusDegrees:
    def __set_name__(self, owner, attr_name):
        self.name = f"celsius_degrees_{attr_name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if not isinstance(val, (float, int)):
            raise ValueError("int or float required")

        if val < -273.15:
            raise ValueError("celsius degrees required")

        return setattr(obj, self.name, val)

    def __delete__(self, obj):
        return delattr(obj, self.name)


class Time:
    def __set_name__(self, owner, attr_name):
        self.name = f"time_{attr_name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if not isinstance(val, str):
            raise ValueError("str required")

        if not re.search("^([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$", val):
            raise ValueError("HH:MM(:SS) required")

        return setattr(obj, self.name, val)

    def __delete__(self, obj):
        return delattr(obj, self.name)
