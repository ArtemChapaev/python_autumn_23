import unittest

from custom_list import CustomList


def check_equality(list1, list2):
    if len(list1) != len(list2):
        return False

    for el1, el2 in zip(list1, list2):
        if el1 != el2:
            return False

    return True


class TestCustomList(unittest.TestCase):
    def test_custom_lists_adding(self):
        actual = CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7])
        expected = CustomList([6, 3, 10, 7])
        self.assertTrue(check_equality(actual, expected))

        actual = CustomList([1]) + [2, 5]
        expected = CustomList([3, 5])
        self.assertTrue(check_equality(actual, expected))

        actual = [2, 5] + CustomList([1])
        expected = CustomList([3, 5])
        self.assertTrue(check_equality(actual, expected))

        actual = CustomList([2, 5]) + [1]
        expected = CustomList([3, 5])
        self.assertTrue(check_equality(actual, expected))

        actual = [1] + CustomList([2, 5])
        expected = CustomList([3, 5])
        self.assertTrue(check_equality(actual, expected))

    def test_custom_lists_subtracting(self):
        actual = CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7])
        expected = CustomList([4, -1, -4, 7])
        self.assertTrue(check_equality(actual, expected))

        actual = CustomList([1]) - [2, 5]
        expected = CustomList([-1, -5])
        self.assertTrue(check_equality(actual, expected))

        actual = [1] - CustomList([2, 5])
        expected = CustomList([-1, -5])
        self.assertTrue(check_equality(actual, expected))

        actual = [2, 5] - CustomList([1])
        expected = CustomList([1, 5])
        self.assertTrue(check_equality(actual, expected))

        actual = CustomList([2, 5]) - [1]
        expected = CustomList([1, 5])
        self.assertTrue(check_equality(actual, expected))

    def test_custom_lists_immutability(self):
        custom_list_a = CustomList([5, 1, 3, 7])
        custom_list_b = CustomList([1, 2, 7])
        list_c = [1, 2]

        copy_custom_list_a = CustomList(custom_list_a)
        copy_custom_list_b = CustomList(custom_list_b)
        copy_list_c = list(list_c)

        custom_list_a + custom_list_b
        self.assertTrue(check_equality(custom_list_a, copy_custom_list_a))
        self.assertTrue(check_equality(custom_list_b, copy_custom_list_b))

        custom_list_b + list_c
        self.assertTrue(check_equality(custom_list_b, copy_custom_list_b))
        self.assertTrue(check_equality(list_c, copy_list_c))

        list_c + custom_list_b
        self.assertTrue(check_equality(list_c, copy_list_c))
        self.assertTrue(check_equality(custom_list_b, copy_custom_list_b))

        custom_list_a - custom_list_b
        self.assertTrue(check_equality(custom_list_a, copy_custom_list_a))
        self.assertTrue(check_equality(custom_list_b, copy_custom_list_b))

        custom_list_b - list_c
        self.assertTrue(check_equality(custom_list_b, copy_custom_list_b))
        self.assertTrue(check_equality(list_c, copy_list_c))

        list_c - custom_list_b
        self.assertTrue(check_equality(list_c, copy_list_c))
        self.assertTrue(check_equality(custom_list_b, copy_custom_list_b))

    def test_custom_lists_comparison(self):
        self.assertTrue(CustomList([5, 1, 3, 7]) > CustomList([1, 2, 7]))
        self.assertTrue(CustomList([5, 1, 3, 7]) == CustomList([7, 2, 7]))
        self.assertTrue(CustomList([5, 1, 3, 7]) < CustomList([10, 2, 7]))
        self.assertTrue(CustomList([5, 1, 3, 7]) >= CustomList([5, 1, 3, 6]))
        self.assertTrue(CustomList([5, 1, 3, 7]) != CustomList([5, 1, 3, 6]))
        self.assertTrue(CustomList([5, 1, 3, 7]) >= CustomList([16]))

        self.assertFalse(CustomList([5, 1, 3, 7]) <= CustomList([1, 2, 7]))
        self.assertFalse(CustomList([5, 1, 3, 7]) > CustomList([7, 2, 7]))
        self.assertFalse(CustomList([5, 1, 3, 7]) >= CustomList([10, 2, 7]))
        self.assertFalse(CustomList([5, 1, 3, 7]) < CustomList([5, 1, 3, 6]))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([5, 1, 3, 6]))
        self.assertFalse(CustomList([5, 1, 3, 7]) != CustomList([16]))

    def test_custom_lists_str(self):
        self.assertEqual(str(CustomList([5, 1, 3, 7])), "[5, 1, 3, 7], sum = 16")
        self.assertEqual(str(CustomList([])), "[], sum = 0")
        self.assertEqual(str(CustomList([0])), "[0], sum = 0")

    def test_custom_lists_error_types(self):
        with self.assertRaises(TypeError) as err:
            CustomList([5, 1, 3, 7]) + 1
        self.assertEqual(type(err.exception), TypeError)

        with self.assertRaises(TypeError) as err:
            CustomList([5, 1, 3, 7]) - "str"
        self.assertEqual(type(err.exception), TypeError)

        with self.assertRaises(TypeError) as err:
            1.1 + CustomList([5, 1, 3, 7])
        self.assertEqual(type(err.exception), TypeError)

        with self.assertRaises(TypeError) as err:
            1.1 > CustomList([5, 1, 3, 7])
        self.assertEqual(type(err.exception), TypeError)

        with self.assertRaises(TypeError) as err:
            [1, 2, 3] > CustomList([5, 1, 3, 7])
        self.assertEqual(type(err.exception), TypeError)

        with self.assertRaises(TypeError) as err:
            [5, 1, 3, 7] == CustomList([5, 1, 3, 7])
        self.assertEqual(type(err.exception), TypeError)


if __name__ == '__main__':
    unittest.main()
