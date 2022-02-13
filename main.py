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

        self.conns = []
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
            self.conns.append(conn)
        return
    
    def recv(self, buffer=1024):
        while self.running:
            for i,conn in enumerate(self.conns):
                data = conn.recv(buffer)
                if data != b'':
                    print(data.decode('UTF-8'))
                    conn.close()
        return

if __name__ == '__main__':
    proxy = ProxyServer(hostname='192.168.0.61')