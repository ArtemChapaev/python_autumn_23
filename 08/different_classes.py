import weakref


class Thing:
    def __call__(self):
        print("It's thing")


class Backpack:
    def __init__(self, passport, lenses, keys, charger, laptop, napkins):
        self.passport = passport
        self.lenses = lenses
        self.keys = keys
        self.charger = charger
        self.laptop = laptop
        self.napkins = napkins


class SlotsBackpack:
    __slots__ = ("passport", "lenses", "keys", "charger", "laptop", "napkins")

    def __init__(self, passport, lenses, keys, charger, laptop, napkins):
        self.passport = passport
        self.lenses = lenses
        self.keys = keys
        self.charger = charger
        self.laptop = laptop
        self.napkins = napkins


class WeakrefBackpack:
    def __init__(self, passport, lenses, keys, charger, laptop, napkins):
        self.passport = weakref.ref(passport)
        self.lenses = weakref.ref(lenses)
        self.keys = weakref.ref(keys)
        self.charger = weakref.ref(charger)
        self.laptop = weakref.ref(laptop)
        self.napkins = weakref.ref(napkins)
