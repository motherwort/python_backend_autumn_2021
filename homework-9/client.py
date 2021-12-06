import sys
import threading
import requests
import socket
import selectors


ADDRESS = ('localhost', 15000)


def read_sys_args():
    argv = sys.argv
    n = int(argv[1])
    filename = argv[2]
    return n, filename


# TODO чтение из файла
def get_urls(filename):
    return ['aaaa', 'bbbb', 'cccc', 'dddd', 'eeee', 'ffff']


class Client:
    def __init__(self, address, n_parallel, urls):
        self.lock = threading.Semaphore(n_parallel)
        self.urls = urls
        self.address = address
        self.received_data = {}

    def run_client(self):
        threads = [
            threading.Thread(target=self.make_request, args=(url,))
            for url in self.urls
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.print_results()
        
    def make_request(self, url):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.address)
        client_socket.send(url.encode())
        data = client_socket.recv(4096)
        self.received_data[url] = data
    
    def print_results(self):
        for url in self.urls:
            data = self.received_data[url].decode()
            print(f'{url}: {data}')


if __name__ == '__main__':
    n, filename = read_sys_args()
    client = Client(ADDRESS, n, get_urls(filename))
    client.run_client()
