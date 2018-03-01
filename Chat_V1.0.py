
import socket
import sys
import threading


class Chat():

    def __init__(self, host=socket . gethostname(), port=5000):
        s = socket.socket(type=socket . SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s = s

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self,param):
        tokens = param.splot(' ')
        if len(tokens) == 2:
            self.__address = (socket.gethostbyaddr(tokens[0])[0], int(tokens[1]))

    def _send(self,param):
        if self.__address is not None:
            message = param.encode()
            totalsent = 0
            while totalsent < len(message):
                sent = self.__s.sendto(message[totalsent:], self.__address)
                totalsent += sent

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                print(data.encode())
            except socket.timeout:
                pass

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/join': self._join,
            '/quit': self._quit,
            '/send': self._send,
        }

        self.__running = True
        self.__address = None

        threading.Thread(target=self._receive).start()

        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            if command in handlers:
                handlers[command]() if param == ' ' else handlers[command](param)
            else:
                print('Uknown command: ', command)
