import asyncio
import sys
import json
from collections import Counter
import time

import aiohttp
from bs4 import BeautifulSoup


def check_arguments():
    arguments = sys.argv
    if len(arguments) != 3 and len(arguments) != 4:
        raise RuntimeError(f"Need 2 or 3 arguments, it has got {len(arguments) - 1}")

    if len(arguments) == 4:
        if arguments[1] == '-c':
            connections_count = arguments[2]
            filename = arguments[3]
        elif arguments[2] == '-c':
            connections_count = arguments[3]
            filename = arguments[1]
        else:
            raise RuntimeError("Need argument -c key")
    else:
        connections_count = arguments[1]
        filename = arguments[2]

    # if error type ValueError will be raised
    connections_count = int(connections_count)

    if connections_count < 1:
        raise ValueError("connections_count must be bigger then 0")

    if not isinstance(filename, str):
        raise TypeError("arguments must be connections count and str (file with urls)")

    return connections_count, filename


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
            for url in file:
                url = url.strip()
                await self.que.put(url)

        await self.que.join()

        for worker in workers:
            worker.cancel()


if __name__ == '__main__':
    num_connections, url_filename = check_arguments()
    fetcher = Fetcher(num_connections)

    asyncio.run(fetcher.start(url_filename))
