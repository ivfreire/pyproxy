# Created by Ícaro Freire on Feb 13th, 2022.
# https://github.com/ivfreire

from asyncio import threads
import sys, socket
from threading import Thread

class ProxyServer:
    def __init__(self, hostname='127.0.0.1', port=9090):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((hostname, port))
        print(f'Proxy server bind to {hostname}:{port}.')

        self.socket.listen(10)
        print('Proxy server is listening...')

        self.sockets = []
        self.running = True

        self.threads = []
        self.threads.append(Thread(target=self.accept, args=[]))
        self.threads.append(Thread(target=self.recv, args=[1024]))

        for thread in self.threads: thread.start()
        for thread in self.threads: thread.join()

        return
    
    def accept(self):
        while self.running:
            conn, addr = self.socket.accept()
            print(f'{addr} has connected.')
            self.sockets.append([conn, None])
        return
    
    def recv(self, buffer=1024):
        while self.running:
            for conn in self.sockets:
                data = conn[0].recv(buffer)
                if data != b'':
                    self.handle(conn, data.decode('ASCII'))
        return
    
    def handle(self, conn, data):
        request = data.split('\n')
        header = request[0].split(' ')
        if header[0] == 'CONNECT': self.connect(conn, request)
        return
    
    def connect(self, conn, request):
        host, port = request[0].split(' ')[1].split(':')
        conn[1] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn[1].connect(( host, int(port) ))
        
        return

if __name__ == '__main__':
    port = 9090
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    proxy = ProxyServer(hostname='192.168.0.61', port=port)