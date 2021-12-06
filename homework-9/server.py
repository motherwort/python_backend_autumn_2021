import sys
import threading
import requests
import socket
import selectors


ADDRESS = ('localhost', 15000)


def read_sys_args():
    argv = sys.argv
    if len(argv) == 1:
        print('Started with 5 workers, 1 keyword')
        return 5, 1
    assert argv[1] == '-w', 'Invalid parameters'
    assert argv[3] == '-k', 'Invalid parameters'
    w = int(argv[2])
    k = int(argv[4])
    print(f'Started with {w} workers, {k} keyword')
    return w, k


class Worker:
    def __init__(self, client_sock, selector, lock=None, post_action=None):
        self.selector = selector
        self.client_sock = client_sock
        self.lock = lock
        self.post_action = post_action
        
    def fit(self, *args, **kwargs):
        thread = threading.Thread(
            target=self._process, 
            args=args,
            kwargs=kwargs
        )
        thread.start()

    def write(self, _):
        if hasattr(self, 'processed_data'):
            if self.processed_data:
                self.client_sock.send(self.processed_data)
                self.selector.unregister(self.client_sock)
                if self.post_action:
                    self.selector.register(self.client_sock, selectors.EVENT_READ, self.post_action)  
                else:
                    self.client_sock.close()
            else:
                self.selector.unregister(self.client_sock)
                self.client_sock.close()
            
    def _process(self, *args, **kwargs):
        if self.lock:
            with self.lock:
                self.processed_data = self.process(*args, **kwargs)
                self.selector.unregister(self.client_sock)
                self.selector.register(
                    self.client_sock, 
                    selectors.EVENT_WRITE, 
                    self.write
                )

    def process(self, *args, **kwargs):
        raise NotImplementedError


def get_url_fetcher(k):
    class UrlFetcher(Worker):
        k_frequent_words = k

        # TODO Воркер обкачивает url по https
        # и возвращает клиенту топ K самых частых слов 
        # и их количества в формате json
        def process(self, data):
            return data.decode().upper().encode()
            
    return UrlFetcher


class Server:
    def __init__(self, address, workers_n, worker_model):
        self.worker_model = worker_model
        self.lock = threading.Semaphore(workers_n)
        self.completed_requests = 0

        self.selector = selectors.DefaultSelector()
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(address)
        self.server_sock.listen()
        
        self.selector.register(self.server_sock, selectors.EVENT_READ, self.accept_conn)

    def run_server(self):
        while True:
            events = self.selector.select()
            for key, _ in events:
                key.data(key.fileobj)

    def accept_conn(self, _):
        client_sock, addr = self.server_sock.accept()
        print('Connect', addr)
        self.selector.register(client_sock, selectors.EVENT_READ, self.read)

    def read(self, client_sock):
        data = client_sock.recv(4096)
        worker = self.worker_model(
            client_sock=client_sock,
            selector=self.selector,
            lock=self.lock,
            post_action=self.post_action
        )
        worker.fit(data)

    def post_action(self, client_sock):
        self.completed_requests += 1
        print(f'{self.completed_requests} requests completed')
        return self.read(self, client_sock)

if __name__ == '__main__':
    w, k = read_sys_args()
    server = Server(ADDRESS, w, get_url_fetcher(k))
    server.run_server()
