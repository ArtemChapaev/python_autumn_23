import unittest
from unittest import mock
import sys
import time
import asyncio

from fetcher import Fetcher, check_arguments


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    async def test_fetcher(self):
        url_count = 68
        texts = [("text" + str(i)).encode() for i in range(url_count)]

        with mock.patch("aiohttp.ClientSession") as mock_session_init:
            mock_session = mock.MagicMock()
            mock_response = mock.AsyncMock()

            async def fake_get(url):
                await asyncio.sleep(0.001)
                return await mock_response

            mock_session_init.return_value.__aenter__.side_effect = [mock_session for _ in range(url_count)]
            mock_session.get.return_value.__aenter__.side_effect = fake_get
            mock_response.text.side_effect = texts

            fetcher = Fetcher(10, 3)
            timestamp1 = time.time()
            await fetcher.start('urls.txt')
            timestamp2 = time.time()

        fetcher_10_connections_time = timestamp2 - timestamp1

        with mock.patch("aiohttp.ClientSession") as mock_session_init:
            mock_session = mock.MagicMock()
            mock_response = mock.AsyncMock()

            async def fake_get(url):
                await asyncio.sleep(0.001)
                return await mock_response

            mock_session_init.return_value.__aenter__.side_effect = [mock_session for _ in range(url_count)]
            mock_session.get.return_value.__aenter__.side_effect = fake_get
            mock_response.text.side_effect = texts

            fetcher = Fetcher(1, 3)
            timestamp1 = time.time()
            await fetcher.start('urls.txt')
            timestamp2 = time.time()

        fetcher_1_connections_time = timestamp2 - timestamp1

        self.assertTrue(fetcher_1_connections_time > fetcher_10_connections_time)

    async def test_one_process_worker(self):
        fetcher = Fetcher(1, 3)
        with mock.patch("builtins.print") as mock_print:
            with mock.patch.object(fetcher, '_process_url') as mock_process_url:
                urls = ['url1', 'url2']
                mock_process_url.side_effect = ['result1', 'result2']

                worker = asyncio.create_task(fetcher._create_process_worker())

                for url in urls:
                    await fetcher.que.put(url)

                await fetcher.que.join()

                worker.cancel()

        expected_calls = [
            mock.call('url1'),
            mock.call('url2')
        ]
        self.assertEqual(mock_process_url.mock_calls, expected_calls)

        expected_calls = [
            mock.call('result1'),
            mock.call('result2')
        ]
        self.assertEqual(mock_print.mock_calls, expected_calls)

    async def test_five_process_workers(self):
        fetcher = Fetcher(2, 3)
        with mock.patch("builtins.print") as mock_print:
            with mock.patch.object(fetcher, '_process_url') as mock_process_url:
                urls = ['url1', 'url2', 'url3', 'url4', 'url5']
                mock_process_url.side_effect = ['result1', 'result2',
                                                'result3', 'result4', 'result5']

                workers = [
                    asyncio.create_task(fetcher._create_process_worker())
                    for _ in range(5)
                ]

                for url in urls:
                    await fetcher.que.put(url)

                await fetcher.que.join()

                for worker in workers:
                    worker.cancel()

        expected_calls = [
            mock.call('url1'),
            mock.call('url2'),
            mock.call('url3'),
            mock.call('url4'),
            mock.call('url5')
        ]
        self.assertEqual(mock_process_url.mock_calls, expected_calls)

        expected_calls = [
            mock.call('result1'),
            mock.call('result2'),
            mock.call('result3'),
            mock.call('result4'),
            mock.call('result5')
        ]
        self.assertEqual(mock_print.mock_calls, expected_calls)

    async def test_five_process_workers_without_data(self):
        fetcher = Fetcher(2, 3)
        with mock.patch("builtins.print") as mock_print:
            with mock.patch.object(fetcher, '_process_url') as mock_process_url:
                # case without data
                urls = []
                mock_process_url.side_effect = []

                workers = [
                    asyncio.create_task(fetcher._create_process_worker())
                    for _ in range(5)
                ]

                for url in urls:
                    await fetcher.que.put(url)

                await fetcher.que.join()

                for worker in workers:
                    worker.cancel()

        mock_process_url.assert_not_called()
        mock_print.assert_not_called()

    def test_fetcher_process_text(self):
        url = 'https://www.wikipedia.org'

        with open('test_html_page.txt', 'r', encoding='utf-8') as file:
            text = "".join(file.readlines())

        fetcher = Fetcher(10, 3)
        self.assertEqual(fetcher._process_text(url, text),
                         'https://www.wikipedia.org: '
                         '[{"your": 3}, {"Wikipedia": 2}, {"reading": 2}]'
                         )

        fetcher = Fetcher(10, 1)
        self.assertEqual(fetcher._process_text(url, text),
                         'https://www.wikipedia.org: [{"your": 3}]'
                         )

    def test_fetcher_process_text_without_data(self):
        url = ''
        text = ''

        fetcher = Fetcher(10, 3)
        self.assertEqual(fetcher._process_text(url, text),"")


class TestFetcherArguments(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetcher_arguments_using(self):
        sys.argv = ('fetcher.py', '-c', '10', 'urls.txt')
        num_connections, url_filename = check_arguments()
        self.assertEqual(num_connections, 10)
        self.assertEqual(url_filename, 'urls.txt')

        sys.argv = ('fetcher.py', 'urls.txt', '-c', '10')
        num_connections, url_filename = check_arguments()
        self.assertEqual(num_connections, 10)
        self.assertEqual(url_filename, 'urls.txt')

        sys.argv = ('fetcher.py', '1', 'urls')
        num_connections, url_filename = check_arguments()
        self.assertEqual(num_connections, 1)
        self.assertEqual(url_filename, 'urls')

    def test_fetcher_arguments_error_using(self):
        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', 'urls', '1')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '-c', 'urls', '1')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(RuntimeError) as err:
            sys.argv = ('fetcher.py', 'urls', '11', '1')
            check_arguments()
        self.assertEqual(RuntimeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '-c', '1')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '1.5', 'urls')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '-1', 'urls')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '0', 'urls')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '-c', '1.5', 'urls')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '-c', '-1', 'urls')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            sys.argv = ('fetcher.py', '-c', '0', 'urls')
            check_arguments()
        self.assertEqual(ValueError, type(err.exception))


if __name__ == '__main__':
    unittest.main()
