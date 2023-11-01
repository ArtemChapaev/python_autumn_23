import unittest
from unittest import mock
import sys

import server
import client


class TestServerArguments(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_server_arguments_using(self):
        sys.argv = ('server.py', '-w', '10', '-k', '7')
        num_workers, top_count = server.check_arguments()
        self.assertEqual(num_workers, 10)
        self.assertEqual(top_count, 7)

        sys.argv = ('server.py', '-k', '7', '-w', '10')
        num_workers, top_count = server.check_arguments()
        self.assertEqual(num_workers, 10)
        self.assertEqual(top_count, 7)

        sys.argv = ('server.py', '-w', '1', '-k', '1')
        num_workers, top_count = server.check_arguments()
        self.assertEqual(num_workers, 1)
        self.assertEqual(top_count, 1)

        sys.argv = ('server.py', '-w', '100', '-k', '100')
        num_workers, top_count = server.check_arguments()
        self.assertEqual(num_workers, 100)
        self.assertEqual(top_count, 100)

    def test_server_arguments_error_using(self):
        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('server.py', '-w', '10')
            server.check_arguments()  # 'server.py', '-w', '10'
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('server.py', '-k', '7', '-w')
            server.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('server.py', '100', '100')
            server.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('server.py', '-k', '7', '-w', '100', '100')
            server.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('server.py', '-k', '7', '-k', '10')
            server.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('server.py', '-w', '1', '-k', '0')
            server.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('server.py', '-w', '0', '-k', '1')
            server.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('server.py', '-w', '-10', '-k', '1')
            server.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('server.py', '-w', '1', '-k', '-10')
            server.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('server.py', '-w', '1.5', '-k', '1')
            server.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('server.py', '-w', '1', '-k', '10.5')
            server.check_arguments()
            self.assertEqual(ValueError, type(err.exception))


class TestClientArguments(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_client_arguments_using(self):
        sys.argv = ('client.py', '10', 'urls.txt')
        num_workers, url_filename = client.check_arguments()
        self.assertEqual(num_workers, 10)
        self.assertEqual(url_filename, 'urls.txt')

        sys.argv = ('client.py', '1', 'urls')
        num_workers, url_filename = client.check_arguments()
        self.assertEqual(num_workers, 1)
        self.assertEqual(url_filename, 'urls')

    def test_client_arguments_error_using(self):
        with self.assertRaises(ValueError) as err:
            sys.argv = ('client.py', 'urls.txt', '10')
            client.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('client.py', 'urls.txt')
            client.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('client.py', 'urls.txt', '11', '11')
            client.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('client.py', '10')
            client.check_arguments()
            self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('client.py', '-1', 'urls.txt')
            client.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('client.py', '0', 'urls.txt')
            client.check_arguments()
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('client.py', '-1.5', 'urls.txt')
            client.check_arguments()
            self.assertEqual(ValueError, type(err.exception))


class TestClientURLs(unittest.TestCase):
    mock_file_content = """\
https://www.wikipedia.org
https://www.ebay.com
"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_client_getting_urls(self):
        with mock.patch(
                'builtins.open',
                new=mock.mock_open(read_data=self.mock_file_content),
                create=True
        ) as mock_open_file:
            urls = client.get_urls_for_processing('urls.txt')
            self.assertEqual(urls, ['https://www.wikipedia.org', 'https://www.ebay.com'])
            mock_open_file.assert_called_once_with('urls.txt', 'r', encoding='utf-8')

    def test_client_getting_urls_error(self):
        with self.assertRaises(FileNotFoundError) as err:
            client.get_urls_for_processing('some_fdsaf.txt')
            self.assertEqual(FileNotFoundError, type(err.exception))


if __name__ == '__main__':
    unittest.main()
