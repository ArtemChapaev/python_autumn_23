import sys
import socket
import threading


def check_arguments():
    arguments = sys.argv
    if len(arguments) != 3:
        raise RuntimeError(f"Need 2 arguments, it has got {len(arguments) - 1}")

    # if error type ValueError will be raised
    threads_count = int(arguments[1])

    if threads_count < 1:
        raise ValueError("threads_count must be bigger then 0")

    return threads_count, arguments[2]


def get_urls_for_processing(filename):
    # in not open FileNotFoundError will be raised
    with open(filename, 'r', encoding='utf-8') as file:
        return [url.strip() for url in file.readlines()]


class Client:
    def __init__(self, threads_limit):
        self.threads_limit = threads_limit

        self.threads = set()
        self.lock = threading.Lock()

    def _check_free_threads(self):
        with self.lock:
            threads_count = len(self.threads)

        return threads_count != self.threads_limit

    @staticmethod
    def _read_data(server_socket):
        data = ""
        read_data = server_socket.recv(1024).decode()

        while len(read_data) == 1024:
            data += read_data
            read_data = server_socket.recv(1024).decode()

        data += read_data

        return data

    def _process_url(self, url):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(("localhost", 5001))

        server_socket.send(url.encode())

        data = self._read_data(server_socket)
        print(data)

        with self.lock:
            self.threads.discard(threading.current_thread())

    def start(self, urls):
        for url in urls:
            # while one thread doesn't become free, we are in this loop
            while True:
                if self._check_free_threads():
                    thread = threading.Thread(target=self._process_url, args=(url,))
                    thread.start()
                    with self.lock:
                        self.threads.add(thread)
                    break

        with self.lock:
            for thread in self.threads:
                thread.join()


if __name__ == '__main__':
    num_threads, url_filename = check_arguments()
    client = Client(num_threads)

    urls_for_processing = get_urls_for_processing(url_filename)
    client.start(urls_for_processing)
