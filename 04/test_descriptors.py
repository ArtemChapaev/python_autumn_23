import unittest

from descriptors import RomanNumber, CelsiusDegrees, Time


class TestRomanNumber(unittest.TestCase):
    class HistoricalEvent:
        century = RomanNumber()

        def __init__(self, century):
            self.century = century

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_roman_number_creating(self):
        event1 = self.HistoricalEvent('X')
        self.assertEqual(event1.century, 'X')

        event2 = self.HistoricalEvent('III')
        self.assertEqual(event2.century, 'III')

        event3 = self.HistoricalEvent('LXIX')
        self.assertEqual(event3.century, 'LXIX')

        event4 = self.HistoricalEvent('MIV')
        self.assertEqual(event4.century, 'MIV')

        event5 = self.HistoricalEvent('MMMCMXCIX')
        self.assertEqual(event5.century, 'MMMCMXCIX')

    def test_roman_number_using(self):
        event = self.HistoricalEvent('X')

        event.century = 'I'
        self.assertEqual(event.century, 'I')

        event.century = 'MI'
        self.assertEqual(event.century, 'MI')

        event.century = 'CMXL'
        self.assertEqual(event.century, 'CMXL')

        event.century = 'XVIII'
        self.assertEqual(event.century, 'XVIII')

        del event.century
        with self.assertRaises(AttributeError) as err:
            event.century
            self.assertEqual(AttributeError, type(err.exception))

        event.century = 'MVII'
        self.assertEqual(event.century, 'MVII')

    def test_roman_number_error_values(self):
        with self.assertRaises(ValueError) as err:
            self.HistoricalEvent(1)
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.HistoricalEvent('str')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.HistoricalEvent('VK')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.HistoricalEvent('IIII')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.HistoricalEvent('IIX')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.HistoricalEvent('IL')
            self.assertEqual(ValueError, type(err.exception))

        event = self.HistoricalEvent('I')
        with self.assertRaises(ValueError) as err:
            event.century = 'LIL'
            self.assertEqual(ValueError, type(err.exception))

        event1 = self.HistoricalEvent('I')
        with self.assertRaises(ValueError) as err:
            event1.century = '1'
            self.assertEqual(ValueError, type(err.exception))

        event2 = self.HistoricalEvent('I')
        with self.assertRaises(ValueError) as err:
            event2.century = 'IVI'
            self.assertEqual(ValueError, type(err.exception))


class TestCelsiusDegrees(unittest.TestCase):
    class Matter:
        boiling_temp = CelsiusDegrees()

        def __init__(self, boiling_temp):
            self.boiling_temp = boiling_temp

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_celsius_degrees_creating(self):
        matter1 = self.Matter(0)
        self.assertEqual(matter1.boiling_temp, 0)

        matter2 = self.Matter(2.124)
        self.assertEqual(matter2.boiling_temp, 2.124)

        matter3 = self.Matter(-240.3)
        self.assertEqual(matter3.boiling_temp, -240.3)

        matter4 = self.Matter(100000)
        self.assertEqual(matter4.boiling_temp, 100000)

        matter5 = self.Matter(-273)
        self.assertEqual(matter5.boiling_temp, -273)

    def test_celsius_degrees_using(self):
        matter = self.Matter(0)

        matter.boiling_temp = 1111
        self.assertEqual(matter.boiling_temp, 1111)

        matter.boiling_temp = -273.15
        self.assertEqual(matter.boiling_temp, -273.15)

        del matter.boiling_temp
        with self.assertRaises(AttributeError) as err:
            matter.boiling_temp
            self.assertEqual(AttributeError, type(err.exception))

        matter.boiling_temp = -1
        self.assertEqual(matter.boiling_temp, -1)

    def test_celsius_degrees_error_values(self):
        with self.assertRaises(ValueError) as err:
            self.Matter('0')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Matter({1: 2.1})
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Matter(-273.16)
            self.assertEqual(ValueError, type(err.exception))

        matter1 = self.Matter(-273)
        with self.assertRaises(ValueError) as err:
            matter1.boiling_temp = {1: 2.1}
            self.assertEqual(ValueError, type(err.exception))

        matter2 = self.Matter(-273)
        with self.assertRaises(ValueError) as err:
            matter2.boiling_temp = -273.16
            self.assertEqual(ValueError, type(err.exception))


class TestTime(unittest.TestCase):

    class Lecture:
        start_time = Time()

        def __init__(self, start_time):
            self.start_time = start_time

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_time_creating(self):
        lecture1 = self.Lecture('09:06')
        self.assertEqual(lecture1.start_time, '09:06')

        lecture2 = self.Lecture('00:00')
        self.assertEqual(lecture2.start_time, '00:00')

        lecture3 = self.Lecture('23:59')
        self.assertEqual(lecture3.start_time, '23:59')

        lecture4 = self.Lecture('17:33')
        self.assertEqual(lecture4.start_time, '17:33')

        lecture5 = self.Lecture('18:38')
        self.assertEqual(lecture5.start_time, '18:38')

    def test_time_using(self):
        lecture = self.Lecture('09:06')

        lecture.start_time = '20:59'
        self.assertEqual(lecture.start_time, '20:59')

        del lecture.start_time
        with self.assertRaises(AttributeError) as err:
            lecture.start_time
            self.assertEqual(AttributeError, type(err.exception))

        lecture.start_time = '23:59'
        self.assertEqual(lecture.start_time, '23:59')

    def test_time_error_values(self):
        with self.assertRaises(ValueError) as err:
            self.Lecture(1)
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Lecture('2300')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Lecture('24:00')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Lecture('-1:00')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Lecture('0:00')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Lecture('1:800')
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.Lecture('18:0')
            self.assertEqual(ValueError, type(err.exception))

        lecture1 = self.Lecture('18:00')
        with self.assertRaises(ValueError) as err:
            lecture1.start_time = '18:0'
            self.assertEqual(ValueError, type(err.exception))

        lecture1 = self.Lecture('18:00')
        with self.assertRaises(ValueError) as err:
            lecture1.start_time = 1800
            self.assertEqual(ValueError, type(err.exception))


if __name__ == '__main__':
    unittest.main()
