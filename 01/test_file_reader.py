import unittest
from unittest import mock

from file_reader import file_reader


class TestFileReader(unittest.TestCase):
    mock_file_content = """\
тесты, тесты и еще раз тесты
python-чик, С++ и тесты
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_file_search(self):
        with mock.patch(
                'builtins.open',
                new=mock.mock_open(read_data=self.mock_file_content),
                create=True
        ) as _:
            gen = file_reader("/tmp/file2", ["тесты"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            self.assertEqual(next(gen), "python-чик, С++ и тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

            gen = file_reader("/tmp/file2", ["раз", "С++"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            self.assertEqual(next(gen), "python-чик, С++ и тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

            gen = file_reader("/tmp/file2", ["раз"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

    def test_file_object_search(self):
        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, ["тесты"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            self.assertEqual(next(gen), "python-чик, С++ и тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, ["раз", "С++"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            self.assertEqual(next(gen), "python-чик, С++ и тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, ["раз"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, ["Раз"])
            self.assertEqual(next(gen), "тесты, тесты и еще раз тесты")
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

    def test_with_special_words(self):
        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, [])
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, [""])
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(file, ["Java", "неправильно"])
            with self.assertRaises(StopIteration) as err:
                next(gen)
                self.assertEqual(StopIteration, type(err.exception))

    def test_with_error_types(self):
        with open("file_reader_test_file.txt", 'r', encoding="UTF-8") as file:
            gen = file_reader(12, ["тесты"])
            with self.assertRaises(TypeError) as err:
                next(gen)
                self.assertEqual(TypeError, type(err.exception))

            gen = file_reader(file, 13)
            with self.assertRaises(TypeError) as err:
                next(gen)
                self.assertEqual(TypeError, type(err.exception))


if __name__ == '__main__':
    unittest.main()
