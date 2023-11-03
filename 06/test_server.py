import unittest
from unittest import mock

from server import Server


class TestServer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # similar code to test_client_check_free_threads in test_client.py
    def test_server_check_free_workers(self):
        server = Server(10, 7)
        self.assertEqual(server._check_free_workers(), True)

        server.worker_threads = set(range(10))
        self.assertEqual(server._check_free_workers(), False)

        server.worker_threads = set(range(9))
        self.assertEqual(server._check_free_workers(), True)

    # similar code to test_client_read_data in test_client.py
    def test_server_read_data(self):
        server = Server(10, 7)

        string_1024 = '1' * 1024

        mock_socket = mock.MagicMock()
        mock_socket.recv.side_effect = [
            'Hello'.encode(),
            (string_1024.encode()), (string_1024.encode()), ('1'.encode())
        ]

        self.assertEqual(server._read_data(mock_socket), 'Hello')

        self.assertEqual(server._read_data(mock_socket), '1' * 2049)

    def test_server_get_top_words_from_url(self):
        with open('test_html_page.txt', 'r', encoding='utf-8') as file:
            text = "".join(file.readlines())

        server = Server(10, 3)
        self.assertEqual(server._get_top_words_from_text(text),
                         '[{"your": 3}, {"Wikipedia": 2}, {"reading": 2}]'
                         )

        server = Server(10, 1)
        self.assertEqual(server._get_top_words_from_text(text),
                         '[{"your": 3}]'
                         )

    def test_process_connection(self):
        url = 'some_url'
        text = 'some_text'
        top_words = 'top top'
        data = url + ": " + top_words

        mock_current_worker_thread_value = 1

        server = Server(10, 7)
        server.worker_threads.add(mock_current_worker_thread_value)

        with mock.patch("builtins.print") as mock_print:
            with mock.patch("threading.current_thread") as mock_current_thread:
                mock_current_thread.return_value = mock_current_worker_thread_value

                with mock.patch.object(server, '_read_data') as mock_read_data:
                    mock_read_data.return_value = url
                    with mock.patch.object(server, '_fetch_url') as mock_fetch_url:
                        mock_fetch_url.return_value = text
                        with mock.patch.object(server, '_get_top_words_from_text'
                                               ) as mock_get_top_words:
                            mock_get_top_words.return_value = top_words

                            mock_client_socket = mock.MagicMock()
                            server._process_connection(mock_client_socket)

                            # _process_connection must read url
                            # and get top_words from _get_top_words_from_text
                            mock_read_data.assert_called_once_with(mock_client_socket)
                            mock_fetch_url.assert_called_once_with(url)
                            mock_get_top_words.assert_called_once_with(text)

                            # _process_connection must send data and close socket
                            mock_client_socket.send.assert_called_once_with(data.encode())
                            mock_client_socket.close.assert_called_once()

                            # _process_connection must increase processed_urls and print it
                            self.assertEqual(server.processed_urls, 1)
                            mock_print.assert_called_once_with("Processed 1 url(s)")

                            # _process_connection must discard current_thread from worker_threads
                            self.assertEqual(server.worker_threads, set())

    def test_process_connection_with_empty_url(self):
        empty_url = ''
        empty_url_data = "URL is empty"

        mock_current_worker_thread_value = 1

        server = Server(10, 7)
        server.worker_threads.add(mock_current_worker_thread_value)

        with mock.patch("builtins.print") as mock_print:
            with mock.patch("threading.current_thread") as mock_current_thread:
                mock_current_thread.return_value = mock_current_worker_thread_value

                with mock.patch.object(server, '_read_data') as mock_read_data:
                    mock_read_data.return_value = empty_url

                    mock_client_socket = mock.MagicMock()
                    server._process_connection(mock_client_socket)

                    # _process_connection must read url
                    mock_read_data.assert_called_once_with(mock_client_socket)

                    # _process_connection must send data and close socket
                    mock_client_socket.send.assert_called_once_with(empty_url_data.encode())
                    mock_client_socket.close.assert_called_once()

                    # _process_connection must increase processed_urls and print it
                    self.assertEqual(server.processed_urls, 1)
                    mock_print.assert_called_once_with("Processed 1 url(s)")

                    # _process_connection must discard current_thread from worker_threads
                    self.assertEqual(server.worker_threads, set())


if __name__ == '__main__':
    unittest.main()
