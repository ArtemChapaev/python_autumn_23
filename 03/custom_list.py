class CustomList(list):

    def __add__(self, other):
        if not isinstance(other, list):
            raise TypeError("other must be list or CustomList")

        if len(self) >= len(other):
            new_custom_list = CustomList(self)
        else:
            new_custom_list = CustomList(other)

        for i, (self_value, other_value) in enumerate(zip(other, self)):
            new_custom_list[i] = self_value + other_value

        return new_custom_list

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, list):
            raise TypeError("other must be list or CustomList")

        if len(self) >= len(other):
            new_custom_list = CustomList(self)
        else:
            new_custom_list = CustomList([-value for value in other])

        for i, (self_value, other_value) in enumerate(zip(self, other)):
            new_custom_list[i] = self_value - other_value

        return new_custom_list

    def __rsub__(self, other):
        if not isinstance(other, list):
            raise TypeError("other must be list or CustomList")

        if len(self) >= len(other):
            new_custom_list = CustomList([-value for value in self])
        else:
            new_custom_list = CustomList(other)

        for i, (self_value, other_value) in enumerate(zip(self, other)):
            new_custom_list[i] = other_value - self_value

        return new_custom_list

    def __eq__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError("other must be CustomList")

        return sum(self) == sum(other)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError("other must be CustomList")

        return sum(self) < sum(other)

    def __gt__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError("other must be CustomList")

        return sum(self) > sum(other)

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return super().__str__() + f", sum = {sum(self)}"
