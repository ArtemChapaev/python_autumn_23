import asyncio
import argparse
import json
from collections import Counter

import aiohttp
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("connections_or_file", nargs='?')
    parser.add_argument("filename", type=str)
    parser.add_argument("-c", "--connections", type=int)

    args = parser.parse_args()

    if args.connections is None:
        connections_count = args.connections
    else:
        connections_count = int(args.connections_or_file)

    return connections_count, args.filename


class Fetcher:
    def __init__(self, connections_count, count_top_words=3):
        self.count_top_words = count_top_words
        self.connections_count = connections_count

    def _process_text(self, url, text):
        filtered_text = BeautifulSoup(text, 'html.parser').get_text()

        words = filtered_text.split()
        most_common_words = Counter(words).most_common(self.count_top_words)

        if not most_common_words:
            return ""

        return url + ": " + json.dumps([{word: count} for word, count in most_common_words])

    async def _process_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()

                return await asyncio.get_event_loop().run_in_executor(
                    None, self._process_text, url, text)

    async def _create_process_worker(self):
        while True:
            url = await self.que.get()
            try:
                result = await self._process_url(url)
                print(result)
            except aiohttp.ClientConnectorError:
                pass
            finally:
                self.que.task_done()

    async def start(self, filename):
        self.que = asyncio.Queue()

        workers = [
            asyncio.create_task(self._create_process_worker())
            for _ in range(self.connections_count)
        ]

        # if not open FileNotFoundError will be raised
        with open(filename, 'r', encoding='utf-8') as file:
            url = file.readline()
            while url:
                await self.que.put(url.strip())
                url = file.readline()

        await self.que.join()

        for worker in workers:
            worker.cancel()


if __name__ == '__main__':
    num_connections, url_filename = parse_arguments()
    fetcher = Fetcher(num_connections)

    asyncio.run(fetcher.start(url_filename))
