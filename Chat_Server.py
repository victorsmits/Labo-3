import socket
import struct
import pickle
import sys

# SERVERADDRESS = (socket.gethostname(), 6000)
SERVERADDRESS = ('0.0.0.0', 6000)


# python main.py server

class Server:
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__clients = {}
        self.__running = False

    def run(self):
        self.__running = True
        self.__s.listen()
        print('Server adress: ', SERVERADDRESS)

        while self.__running:

            client, addr = self.__s.accept()
            clt = self._receive(client)
            print('request:', clt)

            try:
                if clt == 'clients':
                    self._handle(client)

                elif clt == 'disconnect':
                    for i, j in self.__clients.items():
                        if j[0] == addr[0]:
                            x = i
                    del self.__clients[x]

                else:
                    self.__clients[clt] = addr
                    client.send(("{} {} {}".format(clt, addr[0], addr[1])).encode())
                print(self.__clients, '\n')

                client.close()

            except OSError:
                print('Error with the reception of message')

    # fonction receive to get a message from the client
    def _receive(self, client):
        size = struct.unpack('I', client.recv(4))[0]
        data = pickle.loads(client.recv(size)).decode()
        return data

    def _handle(self, client):
        clt = ""
        for i, j in self.__clients.items():
            clt += ("{} {} {}|".format(i, j[0], j[1]))
        client.send(clt.encode())


if __name__ == '__main__':
    Server().run()
