import unittest
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


if __name__ == '__main__':
    unittest.main()
