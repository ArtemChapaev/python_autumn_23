import sys
import socket
import threading
import json
from urllib.request import urlopen
from collections import Counter

from bs4 import BeautifulSoup


def check_arguments():
    arguments = sys.argv
    if len(arguments) != 5:
        raise RuntimeError(f"Need 4 arguments, it has got {len(arguments) - 1}")

    if arguments[1] == '-w':
        workers_count = arguments[2]
    elif arguments[3] == '-w':
        workers_count = arguments[4]
    else:
        raise RuntimeError("Need argument -w key")

    if arguments[1] == '-k':
        count_top_words = arguments[2]
    elif arguments[3] == '-k':
        count_top_words = arguments[4]
    else:
        raise RuntimeError("Need argument with -k key")

    # if error types will be ValueError will be raised
    workers_count = int(workers_count)
    count_top_words = int(count_top_words)

    if workers_count < 1 or count_top_words < 1:
        raise ValueError("Arguments must be bigger then 0")

    return workers_count, count_top_words


class Server:
    def __init__(self, workers_limit, count_top_words):
        self.workers_limit = workers_limit
        self.count_top_words = count_top_words

        self.worker_threads = set()
        self.lock = threading.Lock()
        self.processed_urls = 0

    def _check_free_workers(self):
        with self.lock:
            workers_count = len(self.worker_threads)

        return workers_count != self.workers_limit

    @staticmethod
    def _read_data(client_socket):
        data = ""
        read_data = client_socket.recv(1024).decode()

        while len(read_data) == 1024:
            data += read_data
            read_data = client_socket.recv(1024).decode()

        data += read_data

        return data

    @staticmethod
    def _fetch_url(url):
        with urlopen(url) as response:
            return response.read().decode()

    def _get_top_words_from_text(self, text):
        filtered_text = BeautifulSoup(text, 'html.parser').get_text()
        words = filtered_text.split()

        most_common_words = Counter(words).most_common(self.count_top_words)
        most_common_words = [{word: count} for word, count in most_common_words]

        return json.dumps(most_common_words)

    def _process_connection(self, client_sock):
        url = self._read_data(client_sock)

        text = self._fetch_url(url)
        top_words = self._get_top_words_from_text(text)

        data = url + ": " + top_words

        client_sock.send(data.encode())
        client_sock.close()

        with self.lock:
            self.processed_urls += 1

        print(f"Processed {self.processed_urls} url(s)")

        with self.lock:
            self.worker_threads.discard(threading.current_thread())

    def _start_master(self, server_sock):
        while True:
            # infinite loop
            client_sock, _ = server_sock.accept()

            while True:
                # while one worker doesn't become free, we are in this loop
                if self._check_free_workers():
                    thread = threading.Thread(target=self._process_connection, args=(client_sock,))
                    thread.start()
                    with self.lock:
                        self.worker_threads.add(thread)
                    break

    def start(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("localhost", 5001))
        server_sock.listen()

        self._start_master(server_sock)


if __name__ == '__main__':
    num_workers, top_count = check_arguments()
    server = Server(num_workers, top_count)
    server.start()
