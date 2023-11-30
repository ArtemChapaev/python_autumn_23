import argparse
import socket
import threading
import json
import urllib.request
import urllib.error
from collections import Counter

from bs4 import BeautifulSoup


def check_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--workers", type=int, required=True, nargs=1)
    parser.add_argument("-k", "--k_top_words", type=int, required=True, nargs=1)

    args = parser.parse_args()

    return args.workers[0], args.k_top_words[0]


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
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode()
        except urllib.error.HTTPError:
            return ""

    def _get_top_words_from_text(self, text):
        filtered_text = BeautifulSoup(text, 'html.parser').get_text()
        words = filtered_text.split()

        most_common_words = Counter(words).most_common(self.count_top_words)
        most_common_words = [{word: count} for word, count in most_common_words]

        return json.dumps(most_common_words)

    def _process_connection(self, client_sock):
        url = self._read_data(client_sock)

        if url:
            text = self._fetch_url(url)

            if text:
                data = url + ": " + self._get_top_words_from_text(text)
            else:
                data = url + ": " + 'Error with reading'

            client_sock.send(data.encode())
        else:
            client_sock.send("URL is empty".encode())

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
