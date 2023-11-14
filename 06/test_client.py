import unittest
from unittest import mock
import socket

from client import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # similar code to test_server_check_free_workers test_server.py
    def test_client_check_free_threads(self):
        client = Client(10)
        self.assertEqual(client._check_free_threads(), True)

        client.threads = set(range(10))
        self.assertEqual(client._check_free_threads(), False)

        client.threads = set(range(9))
        self.assertEqual(client._check_free_threads(), True)

    # similar code to test_server_read_data test_server.py
    def test_client_read_data(self):
        client = Client(10)

        string_1024 = '1' * 1024

        mock_socket = mock.MagicMock()
        mock_socket.recv.side_effect = [
            'Hello'.encode(),
            (string_1024.encode()), (string_1024.encode()), ('1'.encode())
        ]

        self.assertEqual(client._read_data(mock_socket), 'Hello')

        self.assertEqual(client._read_data(mock_socket), '1' * 2049)

    def test_client_process_url(self):
        server_answer = 'some_answer'.encode()
        url = 'some_url'
        mock_current_thread_value = 1
        with mock.patch("builtins.print") as mock_print:
            with mock.patch("threading.current_thread") as mock_current_thread:
                mock_current_thread.return_value = mock_current_thread_value
                with mock.patch("socket.socket") as mock_socket_init:
                    mock_server_socket = mock.MagicMock()

                    mock_socket_init.return_value = mock_server_socket
                    mock_server_socket.recv.return_value = server_answer

                    client = Client(10)
                    client.threads.add(mock_current_thread_value)

                    client._process_url(url)

                    # _process_url must create socket, connect to server, send url.encode()
                    mock_socket_init.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
                    mock_server_socket.connect.assert_called_once_with(("localhost", 5001))
                    mock_server_socket.send.assert_called_once_with(url.encode())

                    # _process_url must print server_answer
                    mock_print.assert_called_once_with(server_answer.decode())

                    # client._process_url must discard current_thread from threads
                    self.assertEqual(client.threads, set())


if __name__ == '__main__':
    unittest.main()
