
import socket


class Chat():

    def __init__(self, host=socket . gethostname(), port=5000):
        s = socket.socket(type=socket . SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, ))
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
