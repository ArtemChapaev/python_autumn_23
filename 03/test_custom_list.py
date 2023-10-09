import unittest

from custom_list import CustomList


class MyTestCase(unittest.TestCase):

    def test_custom_list_creating(self):
        CustomList()
        CustomList([1, 2, 4])
        CustomList([1, 2.2, -4])

    def test_custom_lists_adding(self):
        self.assertEqual(CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]),
                         CustomList([6, 3, 10, 7]))

        self.assertEqual(CustomList([1]) + [2, 5], CustomList([3, 5]))
        self.assertEqual([2, 5] + CustomList([1]), CustomList([3, 5]))

    def test_custom_lists_subtracting(self):
        self.assertEqual(CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]),
                         CustomList([4, -1, -4, 7]))

        self.assertEqual(CustomList([1]) - [2, 5], CustomList([-1, -5]))
        self.assertEqual([2, 5] - CustomList([1]), CustomList([1, 5]))

    def test_custom_lists_immutability(self):
        custom_list_a = CustomList([5, 1, 3, 7])
        custom_list_b = CustomList([1, 2, 7])
        list_c = [1, 2]

        copy_custom_list_a = CustomList(custom_list_a)
        copy_custom_list_b = CustomList(custom_list_b)
        copy_list_c = list(list_c)

        custom_list_a + custom_list_b
        self.assertEqual(custom_list_a, copy_custom_list_a)
        self.assertEqual(custom_list_b, copy_custom_list_b)

        custom_list_b + list_c
        self.assertEqual(custom_list_b, copy_custom_list_b)
        self.assertEqual(list_c, copy_list_c)

        list_c + custom_list_b
        self.assertEqual(list_c, copy_list_c)
        self.assertEqual(custom_list_b, copy_custom_list_b)

        custom_list_a - custom_list_b
        self.assertEqual(custom_list_a, copy_custom_list_a)
        self.assertEqual(custom_list_b, copy_custom_list_b)

        custom_list_b - list_c
        self.assertEqual(custom_list_b, copy_custom_list_b)
        self.assertEqual(list_c, copy_list_c)

        list_c - custom_list_b
        self.assertEqual(list_c, copy_list_c)
        self.assertEqual(custom_list_b, copy_custom_list_b)

    def test_custom_lists_comparison(self):
        self.assertEqual(CustomList([5, 1, 3, 7]) > CustomList([1, 2, 7]), True)
        self.assertEqual(CustomList([5, 1, 3, 7]) == CustomList([7, 2, 7]), True)
        self.assertEqual(CustomList([5, 1, 3, 7]) < CustomList([10, 2, 7]), True)
        self.assertEqual(CustomList([5, 1, 3, 7]) >= CustomList([5, 1, 3, 6]), True)
        self.assertEqual(CustomList([5, 1, 3, 7]) != CustomList([5, 1, 3, 6]), True)
        self.assertEqual(CustomList([5, 1, 3, 7]) >= CustomList([16]), True)

        self.assertEqual(CustomList([5, 1, 3, 7]) <= CustomList([1, 2, 7]), False)
        self.assertEqual(CustomList([5, 1, 3, 7]) > CustomList([7, 2, 7]), False)
        self.assertEqual(CustomList([5, 1, 3, 7]) >= CustomList([10, 2, 7]), False)
        self.assertEqual(CustomList([5, 1, 3, 7]) < CustomList([5, 1, 3, 6]), False)
        self.assertEqual(CustomList([5, 1, 3, 7]) == CustomList([5, 1, 3, 6]), False)
        self.assertEqual(CustomList([5, 1, 3, 7]) != CustomList([16]), False)

    def test_custom_lists_str(self):
        self.assertEqual(str(CustomList([5, 1, 3, 7])), "[5, 1, 3, 7], sum = 16")
        self.assertEqual(str(CustomList([])), "[], sum = 0")
        self.assertEqual(str(CustomList([0])), "[0], sum = 0")

    def test_custom_lists_error_types(self):
        with self.assertRaises(TypeError) as err:
            CustomList(False)
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            CustomList(1)
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            CustomList("str")
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            CustomList([5, "str", 3, 7])
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            CustomList([5, 1, 3, 7]) + 1
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            CustomList([5, 1, 3, 7]) - "str"
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            1.1 + CustomList([5, 1, 3, 7])
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            1.1 > CustomList([5, 1, 3, 7])
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            [1, 2, 3] > CustomList([5, 1, 3, 7])
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            [5, 1, 3, 7] == CustomList([5, 1, 3, 7])
            self.assertEqual(TypeError, type(err.exception))


if __name__ == '__main__':
    unittest.main()
