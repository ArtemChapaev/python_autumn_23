import unittest

from custom_meta import CustomMeta


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def _circle(self):
        return 200

    def __triangle(self):
        return 300

    def __str__(self):
        return "Custom_by_metaclass"


class TestCustomMeta(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_custom_meta_class_static(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError) as err:
            CustomClass.x
            self.assertEqual(AttributeError, type(err.exception))

    def test_custom_meta_inst_static(self):
        inst = CustomClass()

        self.assertEqual(inst.custom_x, 50)
        with self.assertRaises(AttributeError) as err:
            inst.x
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst.custom_val, 99)
        with self.assertRaises(AttributeError) as err:
            inst.val
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst.__str__(), "Custom_by_metaclass")
        with self.assertRaises(AttributeError) as err:
            inst.____str__()
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst.custom_line(), 100)
        with self.assertRaises(AttributeError) as err:
            inst.line()
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst._custom_circle(), 200)
        with self.assertRaises(AttributeError) as err:
            inst._circle()
            self.assertEqual(AttributeError, type(err.exception))
        with self.assertRaises(AttributeError) as err:
            inst.custom__circle()
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst.__custom_triangle(), 300)
        with self.assertRaises(AttributeError) as err:
            inst.__triangle()
            self.assertEqual(AttributeError, type(err.exception))
        with self.assertRaises(AttributeError) as err:
            inst.custom___triangle()
            self.assertEqual(AttributeError, type(err.exception))

    def test_custom_meta_inst_dynamic(self):
        inst = CustomClass()

        inst.public = 'public'
        inst._non_public = 'non_public'
        inst.__private = 'private'

        self.assertEqual(inst.custom_public, 'public')
        with self.assertRaises(AttributeError) as err:
            inst.public
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst._custom_non_public, 'non_public')
        with self.assertRaises(AttributeError) as err:
            inst._non_public
            self.assertEqual(AttributeError, type(err.exception))
        with self.assertRaises(AttributeError) as err:
            inst.custom__non_public
            self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(inst.__custom_private, 'private')
        with self.assertRaises(AttributeError) as err:
            inst.__private
            self.assertEqual(AttributeError, type(err.exception))
        with self.assertRaises(AttributeError) as err:
            inst.custom___private
            self.assertEqual(AttributeError, type(err.exception))


if __name__ == '__main__':
    unittest.main()
