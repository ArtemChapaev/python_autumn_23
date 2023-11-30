import argparse
import socket
import threading


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("threads_count", type=int)
    parser.add_argument("filename", type=str)

    args = parser.parse_args()

    print(args.threads_count, args.filename)

    return args.threads_count, args.filename


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
        with self.lock:
            print(data)

        with self.lock:
            self.threads.discard(threading.current_thread())

    def start(self, filename):
        # if not open FileNotFoundError will be raised
        with open(filename, 'r', encoding='utf-8') as file:
            url = file.readline()
            while url:
                url = url.strip()
                # while one thread doesn't become free, we are in this loop
                while True:
                    if self._check_free_threads():
                        thread = threading.Thread(target=self._process_url, args=(url,))
                        thread.start()
                        with self.lock:
                            self.threads.add(thread)
                        break
                url = file.readline()


if __name__ == '__main__':
    num_threads, url_filename = parse_arguments()

    client = Client(num_threads)
    client.start(url_filename)
